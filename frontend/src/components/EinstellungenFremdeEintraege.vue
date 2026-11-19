<template>
  <div>
    <div v-if="!kompakt" class="flex gap-4 items-center mb-2">
      <BaseSubheading>Inhalte teilen</BaseSubheading>
    </div>
    <p v-if="!kompakt" class="text-sm text-gray-600 mb-5">
      Kommunen können Tags, Indikatoren und Textbausteine untereinander austauschen. Hier legen Sie
      fest, ob Ihre Kommune eigene Inhalte teilt und ob Inhalte anderer Kommunen angezeigt werden –
      in den Einstellungen und bei der Auswahl im Mobilitätscheck. Die Einstellungen gelten für alle
      Nutzer:innen Ihrer Kommune.
    </p>
    <Message v-if="!darfAendern" severity="info" icon="pi pi-info-circle" class="mb-4">
      Nur kommunale Administrator:innen können diese Einstellungen ändern.
    </Message>

    <BaseSkeleton v-if="isLoading" :rows="4" />
    <div v-else :class="['flex flex-col', kompakt ? 'gap-4' : 'gap-6']" data-tour="inhalte-teilen">
      <section v-for="gruppe in gruppen" :key="gruppe.titel">
        <h3 class="mb-2 text-xs font-semibold uppercase tracking-wide text-gray-500">
          {{ gruppe.titel }}
        </h3>
        <div
          class="divide-y divide-gray-100 overflow-hidden rounded-xl border border-gray-200 bg-white"
        >
          <div
            v-for="eintrag in gruppe.eintraege"
            :key="eintrag.feld"
            :class="['flex items-center gap-4 px-4', kompakt ? 'py-3' : 'py-4']"
          >
            <span
              class="flex h-9 w-9 shrink-0 items-center justify-center rounded-lg bg-blue-100 text-blue-700"
            >
              <i :class="eintrag.icon" />
            </span>
            <div class="min-w-0 flex-1">
              <label :for="`schalter-${eintrag.feld}`" class="font-medium text-gray-900">
                {{ eintrag.label }}
              </label>
              <p v-if="!kompakt" class="text-sm text-gray-500">{{ eintrag.beschreibung }}</p>
            </div>
            <ToggleSwitch
              :inputId="`schalter-${eintrag.feld}`"
              :modelValue="werte[eintrag.feld]"
              :disabled="!darfAendern || speichertFeld === eintrag.feld"
              @update:modelValue="(wert) => onSpeichern(eintrag, wert)"
            />
          </div>
        </div>
      </section>
    </div>
  </div>
</template>

<script setup>
import { computed, onMounted, ref } from 'vue'
import Message from 'openvue/message'
import ToggleSwitch from 'openvue/toggleswitch'
import { toastService } from '@/services/toast'
import { useAuthStore } from '@/stores/auth'
import { useKommuneEinstellungen } from '@/composables/kommuneEinstellungen'

defineProps({
  // Kompakte Darstellung ohne Überschrift und Beschreibungen, z. B. im Einführungswizard
  kompakt: {
    type: Boolean,
    default: false
  }
})

const gruppen = [
  {
    titel: 'Eigene Inhalte teilen',
    eintraege: [
      {
        feld: 'inhalteTeilen',
        label: 'Teilen mit anderen Kommunen erlauben',
        beschreibung:
          'Nutzer:innen Ihrer Kommune können Tags, Indikatoren und Textbausteine für andere Kommunen sichtbar machen. Ist dies aus, sind alle Inhalte Ihrer Kommune privat – die Einstellung der einzelnen Einträge bleibt erhalten.',
        icon: 'pi pi-share-alt',
        meldung: (wert) =>
          wert
            ? 'Teilen mit anderen Kommunen ist erlaubt'
            : 'Inhalte Ihrer Kommune werden nicht mehr geteilt'
      }
    ]
  },
  {
    titel: 'Inhalte anderer Kommunen anzeigen',
    eintraege: [
      {
        feld: 'fremdeTagsAnzeigen',
        label: 'Tags anderer Kommunen anzeigen',
        beschreibung: 'Geteilte Tags erscheinen in Ihren Listen und Filtern.',
        icon: 'pi pi-tag',
        meldung: (wert) =>
          wert ? 'Tags anderer Kommunen werden angezeigt' : 'Tags anderer Kommunen ausgeblendet'
      },
      {
        feld: 'fremdeIndikatorenAnzeigen',
        label: 'Indikatoren anderer Kommunen anzeigen',
        beschreibung: 'Geteilte Indikatoren können Unterzielen zugeordnet werden.',
        icon: 'pi pi-chart-bar',
        meldung: (wert) =>
          wert
            ? 'Indikatoren anderer Kommunen werden angezeigt'
            : 'Indikatoren anderer Kommunen ausgeblendet'
      },
      {
        feld: 'fremdeTextbausteineAnzeigen',
        label: 'Textbausteine anderer Kommunen anzeigen',
        beschreibung: 'Geteilte Textbausteine können in Erläuterungen eingefügt werden.',
        icon: 'pi pi-align-left',
        meldung: (wert) =>
          wert
            ? 'Textbausteine anderer Kommunen werden angezeigt'
            : 'Textbausteine anderer Kommunen ausgeblendet'
      }
    ]
  }
]

const authStore = useAuthStore()
const darfAendern = computed(() => authStore.istKommunaleAdmin)
const { werte, laden, speichern } = useKommuneEinstellungen()
const isLoading = ref(true)
const speichertFeld = ref(null)

onMounted(async () => {
  try {
    await laden({ neu: true })
  } finally {
    isLoading.value = false
  }
})

const onSpeichern = async (eintrag, wert) => {
  const vorher = werte.value[eintrag.feld]
  werte.value[eintrag.feld] = wert
  speichertFeld.value = eintrag.feld
  try {
    await speichern({ [eintrag.feld]: wert })
    toastService.add({ severity: 'success', detail: eintrag.meldung(wert) })
  } catch {
    werte.value[eintrag.feld] = vorher
    toastService.add({ severity: 'error', detail: 'Einstellung konnte nicht gespeichert werden' })
  } finally {
    speichertFeld.value = null
  }
}
</script>
