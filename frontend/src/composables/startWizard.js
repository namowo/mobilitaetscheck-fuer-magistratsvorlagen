import { ref, computed } from 'vue'
import { apiClient } from '@/services/axios'
import { useAuthStore } from '@/stores/auth'

// Shared state so the wizard can be opened from anywhere (e.g. the profile menu)
const visible = ref(false)
const stepIndex = ref(0)
const status = ref({}) // key -> true (erledigt) | false (offen)
const statusLoaded = ref(false)
// True while the wizard was left (not finished) and can be continued via the floating button
const resumable = ref(false)

const ROLLE_VERWALTUNG = 'verwaltung'
const ROLLE_POLITIK = 'politik'

// ---- Step definitions ------------------------------------------------------
// statusKey: optional key into `status`; steps with a statusKey show "erledigt"/"offen".
// action:    optional router target offered as a button inside the step.

const willkommen = (rolleText) => ({
  key: 'willkommen',
  icon: 'pi pi-compass',
  title: 'Willkommen beim Mobilitätscheck',
  paragraphs: [
    'Mit dem Mobilitätscheck bewerten Sie Magistratsvorlagen systematisch nach den Mobilitäts-Leitzielen Ihrer Kommune – nachvollziehbar, vergleichbar und als PDF exportierbar.',
    rolleText
  ]
})

const STEPS = {
  [ROLLE_VERWALTUNG]: (ctx) => [
    willkommen(
      'Sie haben Verwaltungsrechte. Diese kurze Einführung zeigt Ihnen, wie Sie das Tool für Ihre Kommune einrichten und anschließend nutzen. Sie können sie jederzeit über das Profil-Menü erneut öffnen.'
    ),
    {
      key: 'leitziele',
      icon: 'pi pi-bullseye',
      title: 'Leitziele festlegen',
      statusKey: 'leitziele',
      paragraphs: [
        'Leitziele sind die Grundlage jedes Mobilitätschecks. Ohne eigene Leitziel-Sets kann Ihre Kommune keine Checks durchführen.',
        'Legen Sie ein Leitziel-Set mit Oberzielen und Unterzielen an. Sie können dabei von bestehenden Sets ausgehen.'
      ],
      action: { label: 'Leitziele einrichten', to: { name: 'leitziel-sets' } }
    },
    {
      key: 'gebiete',
      icon: 'pi pi-map',
      title: 'Gebiete pflegen',
      optional: true,
      statusKey: 'gebiete',
      paragraphs: [
        'Mit Gebieten (Stadtteile, Ortsteile) ordnen Sie ein Vorhaben räumlich ein. Die Liste wird einmal gepflegt und steht dann bei jeder Magistratsvorlage zur Auswahl.'
      ],
      action: { label: 'Gebiete verwalten', to: { name: 'gemeinde-gebiet' } }
    },
    {
      key: 'bausteine',
      icon: 'pi pi-book',
      title: 'Textblöcke, Indikatoren und Tags',
      optional: true,
      paragraphs: [
        'Textblöcke sind wiederverwendbare Formulierungen, Indikatoren Regelwerke oder Kennwerte zur Begründung einer Bewertung, Tags Schlagwörter zum Filtern.',
        'Das ist optional – Sie können diese Bausteine auch später beim Arbeiten nach und nach ergänzen.'
      ],
      // Shown individually in the final overview
      checklistItems: [
        { key: 'textbloecke', title: 'Eigene Textblöcke anlegen', statusKey: 'textbloecke', optional: true, action: { label: 'Textblöcke', to: { name: 'textblock' } } },
        { key: 'indikatoren', title: 'Eigene Indikatoren anlegen', statusKey: 'indikatoren', optional: true, action: { label: 'Indikatoren', to: { name: 'indikator' } } },
        { key: 'tags', title: 'Eigene Tags anlegen', statusKey: 'tags', optional: true, action: { label: 'Tags', to: { name: 'tag' } } }
      ],
      actions: [
        { label: 'Textblöcke', to: { name: 'textblock' } },
        { label: 'Indikatoren', to: { name: 'indikator' } },
        { label: 'Tags', to: { name: 'tag' } }
      ]
    },
    {
      key: 'pdf-logo',
      icon: 'pi pi-image',
      title: 'Logo für PDF-Exporte',
      optional: true,
      statusKey: 'pdfLogo',
      paragraphs: [
        'Laden Sie das Logo Ihrer Kommune hoch (PNG oder JPEG, max. 2 MB). Es erscheint auf allen exportierten PDFs.'
      ],
      action: { label: 'Logo hochladen', to: { name: 'pdf-logo' } }
    },
    {
      key: 'team',
      icon: 'pi pi-users',
      title: 'Kolleg:innen und Politik einladen',
      optional: true,
      paragraphs: [
        'Unter „Einstellungen“ erstellen Sie Einladungslinks für Verwaltung und Politik, organisieren Gruppen (z. B. Fachbereiche oder Fraktionen) und verwalten Accounts.'
      ],
      action: { label: 'Einladungen verwalten', to: { name: 'einladungen' } }
    },
    {
      key: 'ablauf',
      icon: 'pi pi-list-check',
      title: 'So läuft ein Check ab',
      paragraphs: [
        '1. Magistratsvorlage anlegen und Gebiet zuordnen.',
        '2. Mobilitätscheck erstellen: Jedes Unterziel bewerten und die Auswirkung begründen.',
        ctx.klimacheckAktiv
          ? '3. Optional: Klimacheck bzw. Klimarelevanzprüfung ergänzen (für Ihre Kommune freigeschaltet).'
          : '3. Ergebnis ansehen und als PDF exportieren.',
        ctx.klimacheckAktiv
          ? '4. Ergebnis ansehen und als PDF exportieren.'
          : 'Weitere Hilfe finden Sie jederzeit in der Dokumentation.'
      ].filter(Boolean),
      statusKey: 'eigeneChecks',
      action: { label: 'Erste Magistratsvorlage anlegen', to: { name: 'magistratsvorlage-neu' } }
    },
    {
      key: 'uebersicht',
      icon: 'pi pi-check-square',
      title: 'Ihre Einrichtung im Überblick',
      checklist: true,
      paragraphs: []
    }
  ],

  [ROLLE_POLITIK]: () => [
    willkommen(
      'Sie haben Zugriff als Politik. Hier erfahren Sie, was Sie im Tool sehen und tun können.'
    ),
    {
      key: 'vorlagen',
      icon: 'pi pi-file',
      title: 'Magistratsvorlagen einsehen',
      paragraphs: [
        'Unter „Magistratsvorlagen“ finden Sie die Vorlagen Ihrer Kommune samt veröffentlichtem Mobilitätscheck.',
        'Sie sehen auf einen Blick, wie sich ein Vorhaben auf jedes Leitziel auswirkt, und können die Begründung nachlesen.'
      ],
      action: { label: 'Zu den Magistratsvorlagen', to: { name: 'magistratsvorlage-liste' } }
    },
    {
      key: 'auswertung',
      icon: 'pi pi-chart-bar',
      title: 'Bewertung verstehen',
      paragraphs: [
        'Jedes Unterziel wird mit einer Auswirkung bewertet und begründet. Indikatoren verweisen auf Regelwerke oder Kennwerte, die die Einschätzung stützen.',
        'Die Ergebnisse lassen sich als PDF herunterladen und in Sitzungsunterlagen verwenden.'
      ]
    },
    {
      key: 'profil',
      icon: 'pi pi-user',
      title: 'Ihr Profil und Ihre Gruppe',
      paragraphs: [
        'Im Profil pflegen Sie Ihre Daten und wählen Ihre Gruppe (z. B. Fraktion oder Partei).'
      ],
      action: { label: 'Profil öffnen', to: { name: 'profil' } }
    }
  ]
}

export const useStartWizard = () => {
  const authStore = useAuthStore()

  // No wizard in the Systemadministration view; when a Systemadmin switches the view to
  // Verwaltung or Politik, the wizard for that role is available (e.g. to demo it).
  const available = computed(() => authStore.effectiveRolleId !== 3)

  const rolle = computed(() => {
    const r = authStore.effectiveRolleId
    if (r === 1 || authStore.effectiveIsLocalSuperuser) return ROLLE_VERWALTUNG
    return ROLLE_POLITIK
  })

  // Verwaltung has set up Leitziele and created a first Mobilitätscheck -> setup is complete
  const setupComplete = computed(
    () =>
      rolle.value === ROLLE_VERWALTUNG &&
      statusLoaded.value &&
      !!status.value.leitziele &&
      !!status.value.eigeneChecks
  )

  const steps = computed(() =>
    STEPS[rolle.value]({ klimacheckAktiv: authStore.klimacheckAktiv })
  )

  const currentStep = computed(() => steps.value[stepIndex.value])
  const isFirst = computed(() => stepIndex.value === 0)
  const isLast = computed(() => stepIndex.value === steps.value.length - 1)

  // ---- Persistence (per user) ----
  const key = (name) => `startWizard:${name}:${authStore.userId}`
  const read = (name) => {
    try {
      return localStorage.getItem(key(name))
    } catch {
      return null
    }
  }
  const write = (name, value) => {
    try {
      localStorage.setItem(key(name), value)
    } catch {
      /* ignore */
    }
  }

  // ---- Status loading ----
  const loadStatus = async () => {
    const s = {}
    if (rolle.value === ROLLE_VERWALTUNG) {
      const [ziel, gebiete, logo, checks, textbloecke, indikatoren, tags] = await Promise.all([
        apiClient.get('/einstellungen/mobilitaetscheck/ziel-set/hat-eigene').catch(() => null),
        apiClient.get('/einstellungen/gebiet').catch(() => null),
        apiClient
          .get('/einstellungen/pdf-logo', { responseType: 'blob', validateStatus: () => true })
          .catch(() => null),
        apiClient.get('/mobilitaetscheck/eingabe/hat-eigene').catch(() => null),
        apiClient.get('/einstellungen/textblock').catch(() => null),
        apiClient.get('/einstellungen/indikator').catch(() => null),
        apiClient.get('/einstellungen/tag').catch(() => null)
      ])
      // These lists also contain platform-wide entries; only the Kommune's own count as done
      const hatEigene = (res) =>
        Array.isArray(res?.data) && res.data.some((i) => i.gemeindeId === authStore.gemeindeId)
      s.leitziele = !!ziel?.data?.hatEigene
      s.gebiete = Array.isArray(gebiete?.data) && gebiete.data.length > 0
      s.pdfLogo = logo?.status === 200
      s.eigeneChecks = !!checks?.data?.hatEigene
      s.textbloecke = hatEigene(textbloecke)
      s.indikatoren = hatEigene(indikatoren)
      s.tags = hatEigene(tags)
    }
    status.value = s
    statusLoaded.value = true
  }

  // ---- Public actions ----
  const open = async (startAt = null) => {
    if (!available.value) return
    await loadStatus()
    const saved = Number(read('step'))
    stepIndex.value =
      startAt ?? (Number.isInteger(saved) && saved > 0 && saved < steps.value.length ? saved : 0)
    // A deliberate (re)start counts as "not done" again, so leaving it midway shows the
    // continue message even if the wizard was finished or dismissed before.
    write('done', 'false')
    resumable.value = false
    visible.value = true
  }

  const close = () => {
    write('step', String(stepIndex.value))
    visible.value = false
    // finish() marks the wizard done before the dialog's @hide calls close() again
    resumable.value = read('done') !== 'true'
  }

  const finish = () => {
    write('done', 'true')
    resumable.value = false
    stepIndex.value = 0 // so the @hide handler persists step 0
    visible.value = false
  }

  const skip = finish

  const resume = () => open()

  const next = () => {
    if (!isLast.value) stepIndex.value++
  }
  const prev = () => {
    if (!isFirst.value) stepIndex.value--
  }

  // Auto-open on first login, or when essential setup is still missing and the user
  // has not explicitly dismissed the wizard.
  const autoOpenIfNeeded = async () => {
    if (!available.value) return
    if (!authStore.isLoggedIn || !authStore.isVerified || !authStore.userId) return
    if (visible.value || read('done') === 'true') return
    await loadStatus()
    // Resume where the user left off (e.g. after following a step's action link or a page reload)
    const saved = Number(read('step'))
    stepIndex.value = Number.isInteger(saved) && saved > 0 && saved < steps.value.length ? saved : 0
    resumable.value = false
    visible.value = true
  }

  return {
    available,
    setupComplete,
    refreshStatus: loadStatus,
    visible,
    stepIndex,
    status,
    statusLoaded,
    resumable,
    rolle,
    steps,
    currentStep,
    isFirst,
    isLast,
    open,
    close,
    resume,
    finish,
    skip,
    next,
    prev,
    autoOpenIfNeeded
  }
}
