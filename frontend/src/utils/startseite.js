// Section ("Abschnitt") model of the configurable Startseite.
// Every block has: id, typ, sichtbar, hintergrund – plus type-specific fields.
// Keys must stay plain identifiers: the axios case converter maps them to snake_case
// on the way to the backend and back to camelCase on the way out.

import { STARTSEITE_STANDARD_TITEL, STARTSEITE_STANDARD_UNTERTITEL } from '@/utils/standardInhalte'

export const neueId = () =>
  window.crypto?.randomUUID?.() ?? `${Date.now().toString(36)}-${Math.random().toString(36).slice(2)}`

// ---------------------------------------------------------------------------
// Links / Buttons
// ---------------------------------------------------------------------------

export const LINK_ZIELE = [
  { label: 'Veröffentlichte Magistratsvorlagen', value: 'oeffentlich-magistratsvorlagen' },
  { label: 'Über das Tool', value: 'ueber-das-tool' },
  { label: 'Dokumentation', value: 'dokumentation' },
  { label: 'Registrieren', value: 'registrieren' },
  { label: 'Anmelden', value: 'anmelden' },
  { label: 'Eigene Adresse (URL)', value: 'extern' }
]

export const BUTTON_STILE = [
  { label: 'Hervorgehoben', value: 'primaer' },
  { label: 'Dezent', value: 'sekundaer' }
]

export const neuerLink = (overrides = {}) => ({
  id: neueId(),
  label: '',
  ziel: 'oeffentlich-magistratsvorlagen',
  url: '',
  stil: 'primaer',
  ...overrides
})

// ---------------------------------------------------------------------------
// Section backgrounds
// ---------------------------------------------------------------------------

export const HINTERGRUENDE = [
  { label: 'Keiner', value: 'keiner' },
  { label: 'Grau', value: 'grau' },
  { label: 'Akzent hell', value: 'akzent-hell' },
  { label: 'Akzent kräftig', value: 'akzent' }
]

// ---------------------------------------------------------------------------
// Icons offered for tiles and figures (PrimeIcons)
// ---------------------------------------------------------------------------

export const ICONS = [
  'pi-car', 'pi-truck', 'pi-map', 'pi-map-marker', 'pi-directions', 'pi-compass', 'pi-globe',
  'pi-building', 'pi-building-columns', 'pi-home', 'pi-users', 'pi-user', 'pi-id-card',
  'pi-file', 'pi-file-check', 'pi-file-edit', 'pi-file-pdf', 'pi-folder-open', 'pi-book',
  'pi-check-circle', 'pi-check-square', 'pi-list-check', 'pi-clipboard', 'pi-chart-bar',
  'pi-chart-line', 'pi-chart-pie', 'pi-gauge', 'pi-sliders-h', 'pi-filter', 'pi-search',
  'pi-eye', 'pi-lock-open', 'pi-shield', 'pi-star', 'pi-heart', 'pi-bolt', 'pi-sun',
  'pi-cloud', 'pi-flag', 'pi-thumbs-up', 'pi-comments', 'pi-megaphone', 'pi-lightbulb',
  'pi-question-circle', 'pi-info-circle', 'pi-calendar', 'pi-clock', 'pi-send', 'pi-share-alt',
  'pi-link', 'pi-sitemap', 'pi-cog', 'pi-wrench', 'pi-database', 'pi-desktop', 'pi-mobile',
  'pi-video', 'pi-play-circle'
].map((name) => `pi ${name}`)

// ---------------------------------------------------------------------------
// Figures (Kennzahlen)
// ---------------------------------------------------------------------------

export const KENNZAHL_QUELLEN = [
  { label: 'Veröffentlichte Magistratsvorlagen (automatisch)', value: 'magistratsvorlagen' },
  { label: 'Veröffentlichte Mobilitätschecks (automatisch)', value: 'mobilitaetschecks' },
  { label: 'Kommunen mit Veröffentlichungen (automatisch)', value: 'gemeinden' },
  { label: 'Eigener Wert', value: 'manuell' }
]

// ---------------------------------------------------------------------------
// Block types
// ---------------------------------------------------------------------------

const basis = (typ, hintergrund = 'keiner') => ({ id: neueId(), typ, sichtbar: true, hintergrund })

export const BLOCK_TYPEN = {
  hero: {
    label: 'Einstieg (Hero)',
    icon: 'pi pi-star',
    beschreibung: 'Großer Titel mit Untertitel, Buttons und optionalem Bild.',
    neu: () => ({
      ...basis('hero'),
      titel: 'Titel',
      untertitel: '',
      layout: 'zentriert',
      bildUrl: '',
      buttons: [neuerLink({ label: 'Magistratsvorlagen ansehen' })]
    })
  },
  text: {
    label: 'Text',
    icon: 'pi pi-align-left',
    beschreibung: 'Freier Text mit Formatierung, Links, Bildern und Tabellen.',
    neu: () => ({ ...basis('text'), titel: '', inhalt: '' })
  },
  video: {
    label: 'Video',
    icon: 'pi pi-video',
    beschreibung: 'YouTube- oder Vimeo-Video, das erst nach Zustimmung geladen wird.',
    neu: () => ({
      ...basis('video'),
      titel: '',
      text: '',
      url: '',
      vorschaubildUrl: '',
      bildunterschrift: '',
      seitenverhaeltnis: '16:9'
    })
  },
  kacheln: {
    label: 'Kacheln',
    icon: 'pi pi-th-large',
    beschreibung: 'Raster aus Karten mit Icon, Titel, Text und optionalem Link.',
    neu: () => ({
      ...basis('kacheln'),
      titel: '',
      untertitel: '',
      spalten: 3,
      kacheln: [neueKachel(), neueKachel(), neueKachel()]
    })
  },
  kennzahlen: {
    label: 'Kennzahlen',
    icon: 'pi pi-chart-bar',
    beschreibung: 'Animierte Zahlen – automatisch aus der Datenbank oder eigene Werte.',
    neu: () => ({
      ...basis('kennzahlen', 'akzent-hell'),
      titel: '',
      nullwerteAusblenden: true,
      eintraege: [
        neueKennzahl({ quelle: 'magistratsvorlagen', label: 'veröffentlichte Magistratsvorlagen', icon: 'pi pi-file' }),
        neueKennzahl({ quelle: 'mobilitaetschecks', label: 'Mobilitätschecks', icon: 'pi pi-check-circle' }),
        neueKennzahl({ quelle: 'gemeinden', label: 'Kommunen', icon: 'pi pi-building' })
      ]
    })
  },
  schritte: {
    label: 'Schritte',
    icon: 'pi pi-list-check',
    beschreibung: 'Nummerierter Ablauf, z. B. „So funktioniert’s“.',
    neu: () => ({
      ...basis('schritte'),
      titel: 'So funktioniert’s',
      untertitel: '',
      schritte: [neuerSchritt(), neuerSchritt(), neuerSchritt()]
    })
  },
  faq: {
    label: 'Häufige Fragen (FAQ)',
    icon: 'pi pi-question-circle',
    beschreibung: 'Aufklappbare Fragen und Antworten.',
    neu: () => ({ ...basis('faq'), titel: 'Häufige Fragen', eintraege: [neueFrage()] })
  },
  aufruf: {
    label: 'Handlungsaufruf',
    icon: 'pi pi-megaphone',
    beschreibung: 'Auffälliges Banner mit Text und Buttons.',
    neu: () => ({
      ...basis('aufruf', 'akzent'),
      titel: 'Titel',
      text: '',
      buttons: [neuerLink({ label: 'Jetzt registrieren', ziel: 'registrieren' })]
    })
  }
}

export function neueKachel(overrides = {}) {
  return { id: neueId(), icon: 'pi pi-star', titel: '', text: '', link: null, ...overrides }
}

export function neueKennzahl(overrides = {}) {
  return { id: neueId(), quelle: 'manuell', wert: 0, suffix: '', label: '', icon: '', ...overrides }
}

export function neuerSchritt(overrides = {}) {
  return { id: neueId(), titel: '', text: '', ...overrides }
}

export function neueFrage(overrides = {}) {
  return { id: neueId(), frage: '', antwort: '', ...overrides }
}

// Deep copy with fresh ids (for "Duplizieren")
export function dupliziereBlock(block) {
  const kopie = JSON.parse(JSON.stringify(block))
  kopie.id = neueId()
  for (const liste of ['kacheln', 'eintraege', 'schritte', 'buttons']) {
    if (Array.isArray(kopie[liste])) kopie[liste].forEach((e) => (e.id = neueId()))
  }
  return kopie
}

// ---------------------------------------------------------------------------
// Default layout. Previous single-field content (Titel/Untertitel/Text) is carried
// over so existing installations keep what they configured.
// ---------------------------------------------------------------------------

export function standardBloecke(einstellung = {}) {
  const bloecke = [
    {
      ...BLOCK_TYPEN.hero.neu(),
      titel: einstellung.startseiteTitel || STARTSEITE_STANDARD_TITEL,
      untertitel: einstellung.startseiteUntertitel || STARTSEITE_STANDARD_UNTERTITEL,
      buttons: [
        neuerLink({ label: 'Magistratsvorlagen ansehen', ziel: 'oeffentlich-magistratsvorlagen' }),
        neuerLink({ label: 'Über das Tool', ziel: 'ueber-das-tool', stil: 'sekundaer' })
      ]
    }
  ]

  if (einstellung.startseiteInhalt) {
    bloecke.push({ ...BLOCK_TYPEN.text.neu(), inhalt: einstellung.startseiteInhalt })
  }

  bloecke.push(
    BLOCK_TYPEN.kennzahlen.neu(),
    {
      ...BLOCK_TYPEN.schritte.neu(),
      untertitel: 'Vom Entwurf der Vorlage bis zur transparenten Veröffentlichung.',
      schritte: [
        neuerSchritt({
          titel: 'Magistratsvorlage erfassen',
          text: 'Die Verwaltung legt die Vorlage mit den wichtigsten Eckdaten an.'
        }),
        neuerSchritt({
          titel: 'Mobilitätscheck durchführen',
          text: 'Die Auswirkungen auf die mobilitätspolitischen Leitziele werden strukturiert bewertet.'
        }),
        neuerSchritt({
          titel: 'Ergebnis veröffentlichen',
          text: 'Politik und Öffentlichkeit sehen die Bewertung – ohne Anmeldung.'
        })
      ]
    },
    {
      ...BLOCK_TYPEN.kacheln.neu(),
      hintergrund: 'grau',
      titel: 'Für wen ist das Tool?',
      kacheln: [
        neueKachel({
          icon: 'pi pi-building-columns',
          titel: 'Verwaltung',
          text: 'Mobilitätswirkungen von Vorlagen einheitlich und nachvollziehbar bewerten.'
        }),
        neueKachel({
          icon: 'pi pi-users',
          titel: 'Kommunalpolitik',
          text: 'Entscheidungen auf Basis einer transparenten Einschätzung treffen.'
        }),
        neueKachel({
          icon: 'pi pi-eye',
          titel: 'Öffentlichkeit',
          text: 'Veröffentlichte Mobilitätschecks jederzeit einsehen.',
          link: neuerLink({ label: 'Zu den Vorlagen', ziel: 'oeffentlich-magistratsvorlagen' })
        })
      ]
    }
  )

  return bloecke
}

// ---------------------------------------------------------------------------
// Video URLs → privacy-friendly embed URLs
// ---------------------------------------------------------------------------

export const VIDEO_ANBIETER = {
  youtube: {
    name: 'YouTube',
    datenempfaenger: 'Google Ireland Limited (YouTube)'
  },
  vimeo: {
    name: 'Vimeo',
    datenempfaenger: 'Vimeo.com, Inc.'
  }
}

function parseStartzeit(wert) {
  if (!wert) return 0
  if (/^\d+$/.test(wert)) return Number(wert)
  const m = /^(?:(\d+)h)?(?:(\d+)m)?(?:(\d+)s)?$/.exec(wert)
  if (!m) return 0
  return Number(m[1] || 0) * 3600 + Number(m[2] || 0) * 60 + Number(m[3] || 0)
}

/**
 * Turn a pasted YouTube/Vimeo link into an embed description.
 * Returns null for anything that isn't a recognised video link.
 * The embed URL never autoplays; the player adds `autoplay=1` after a click.
 */
export function parseVideoUrl(eingabe) {
  if (!eingabe) return null
  let url
  try {
    url = new URL(eingabe.trim())
  } catch {
    return null
  }
  if (url.protocol !== 'https:' && url.protocol !== 'http:') return null
  const host = url.hostname.replace(/^(www|m)\./, '')

  if (['youtube.com', 'youtube-nocookie.com', 'music.youtube.com', 'youtu.be'].includes(host)) {
    let id =
      host === 'youtu.be'
        ? url.pathname.slice(1).split('/')[0]
        : url.searchParams.get('v') ||
          /^\/(?:embed|shorts|live|v)\/([\w-]{11})/.exec(url.pathname)?.[1]
    if (!id || !/^[\w-]{11}$/.test(id)) return null
    const start = parseStartzeit(url.searchParams.get('t') || url.searchParams.get('start'))
    const params = new URLSearchParams({ rel: '0' })
    if (start) params.set('start', String(start))
    return {
      anbieter: 'youtube',
      id,
      embedUrl: `https://www.youtube-nocookie.com/embed/${id}?${params}`
    }
  }

  if (host === 'vimeo.com' || host === 'player.vimeo.com') {
    const m = /\/(\d{5,})(?:\/([\da-f]{6,}))?(?:\/|$)/.exec(url.pathname)
    if (!m) return null
    const params = new URLSearchParams({ dnt: '1' })
    const hash = m[2] || url.searchParams.get('h')
    if (hash) params.set('h', hash)
    return {
      anbieter: 'vimeo',
      id: m[1],
      embedUrl: `https://player.vimeo.com/video/${m[1]}?${params}`
    }
  }

  return null
}

export const VIDEO_DATENSCHUTZ_TEXTVORSCHLAG = `<h3>Eingebettete Videos (YouTube, Vimeo)</h3>
<p>Auf der Startseite binden wir Videos der Plattformen YouTube (Google Ireland Limited, Gordon House, Barrow Street, Dublin 4, Irland) bzw. Vimeo (Vimeo.com, Inc., 330 West 34th Street, New York, NY 10001, USA) ein. Die Videos werden erst geladen, wenn Sie aktiv auf „Video laden“ klicken (Zwei-Klick-Lösung). Vorher werden keine Daten an den jeweiligen Anbieter übertragen.</p>
<p>Mit dem Klick wird eine Verbindung zu den Servern des Anbieters hergestellt. Dabei werden u. a. Ihre IP-Adresse, die aufgerufene Seite sowie technische Informationen zu Ihrem Browser übermittelt. YouTube-Videos binden wir im „erweiterten Datenschutzmodus“ (youtube-nocookie.com) ein, Vimeo-Videos mit aktivierter „Do Not Track“-Option. Eine Übermittlung in Drittländer (insbesondere die USA) kann nicht ausgeschlossen werden.</p>
<p>Rechtsgrundlage ist Ihre Einwilligung gemäß Art. 6 Abs. 1 lit. a DSGVO und § 25 Abs. 1 TDDDG, die Sie durch den Klick erteilen. Haben Sie die Option „immer laden“ gewählt, wird diese Entscheidung lokal in Ihrem Browser gespeichert; Sie können sie widerrufen, indem Sie die Website-Daten Ihres Browsers für diese Seite löschen.</p>`

// Figures that are actually shown: resolves automatic sources and drops zero values if wanted
export function sichtbareKennzahlen(block, kennzahlen) {
  return (block.eintraege || [])
    .map((e) => ({
      ...e,
      zahl: e.quelle === 'manuell' ? Number(e.wert) || 0 : (kennzahlen?.[e.quelle] ?? null)
    }))
    .filter((e) => e.zahl !== null && !(block.nullwerteAusblenden && e.zahl === 0))
}
