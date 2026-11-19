<template>
  <div>
    <div class="flex flex-wrap items-center gap-2 mb-2">
      <BaseSubheading>Startseite</BaseSubheading>
      <Tag v-if="hatAenderungen" severity="warn" value="Ungespeicherte Änderungen" />
    </div>
    <p class="text-sm text-gray-600 mb-5">
      Die Startseite besteht aus Abschnitten, die Sie hinzufügen, anordnen, ausblenden und bearbeiten
      können. Abschnitte ohne Inhalt (z. B. ein Video ohne gültigen Link) werden öffentlich nicht
      angezeigt.
    </p>

    <BaseSkeleton v-if="isLoading" variant="form" :rows="4" />
    <template v-else>
      <!-- Toolbar -->
      <div class="flex flex-wrap items-center gap-2 mb-4">
        <Button
          label="Abschnitt hinzufügen"
          icon="pi pi-plus"
          aria-haspopup="true"
          aria-controls="startseite-abschnitt-menu"
          @click="(e) => hinzufuegenMenu.toggle(e)"
        />
        <Menu id="startseite-abschnitt-menu" ref="hinzufuegenMenu" :model="hinzufuegenItems" popup>
          <template #item="{ item, props: itemProps }">
            <a v-bind="itemProps.action" class="flex items-start gap-3 !py-2">
              <i :class="[item.icon, 'mt-1 text-[var(--p-primary-600)]']" />
              <span class="flex flex-col">
                <span class="font-medium">{{ item.label }}</span>
                <small class="text-gray-500 max-w-64">{{ item.beschreibung }}</small>
              </span>
            </a>
          </template>
        </Menu>
        <Button label="Vorschau" icon="pi pi-eye" outlined @click="vorschauOffen = true" />
        <Button
          v-if="bloecke.length > 1"
          :label="alleZugeklappt ? 'Alle aufklappen' : 'Alle zuklappen'"
          :icon="alleZugeklappt ? 'pi pi-angle-double-down' : 'pi pi-angle-double-up'"
          text
          severity="secondary"
          @click="alleUmschalten"
        />
      </div>

      <!-- Sections -->
      <div v-if="bloecke.length === 0" class="text-sm text-gray-400 text-center py-10 border-2 border-dashed rounded-lg">
        Noch keine Abschnitte. Fügen Sie über „Abschnitt hinzufügen“ den ersten hinzu.
      </div>
      <draggable
        v-else
        :list="bloecke"
        item-key="id"
        handle=".abschnitt-griff"
        class="flex flex-col gap-3"
      >
        <template #item="{ element: block, index }">
          <Panel
            :ref="(el) => (panelRefs[block.id] = el)"
            toggleable
            :collapsed="!offen.has(block.id)"
            :class="{ 'opacity-60': !block.sichtbar }"
            @update:collapsed="(zu) => umschalten(block.id, !zu)"
          >
            <template #header>
              <div
                class="flex items-center gap-3 min-w-0 flex-1 cursor-pointer select-none"
                @click="umschalten(block.id, !offen.has(block.id))"
              >
                <i
                  class="pi pi-bars abschnitt-griff cursor-move text-gray-400"
                  title="Ziehen zum Verschieben"
                  @click.stop
                />
                <span
                  class="flex items-center justify-center w-8 h-8 rounded-md bg-[var(--p-primary-50)] text-[var(--p-primary-600)] shrink-0"
                >
                  <i :class="BLOCK_TYPEN[block.typ]?.icon" />
                </span>
                <div class="flex flex-col min-w-0">
                  <span class="font-semibold">{{ BLOCK_TYPEN[block.typ]?.label ?? block.typ }}</span>
                  <span v-if="zusammenfassung(block)" class="text-sm text-gray-500 truncate">
                    {{ zusammenfassung(block) }}
                  </span>
                </div>
                <Tag v-if="!block.sichtbar" value="Ausgeblendet" severity="secondary" class="shrink-0" />
              </div>
            </template>
            <template #icons>
              <div class="flex items-center">
                <Button
                  icon="pi pi-arrow-up"
                  text
                  rounded
                  severity="secondary"
                  :disabled="index === 0"
                  v-tooltip.top="'Nach oben'"
                  aria-label="Abschnitt nach oben"
                  @click="verschieben(index, -1)"
                />
                <Button
                  icon="pi pi-arrow-down"
                  text
                  rounded
                  severity="secondary"
                  :disabled="index === bloecke.length - 1"
                  v-tooltip.top="'Nach unten'"
                  aria-label="Abschnitt nach unten"
                  @click="verschieben(index, 1)"
                />
                <Button
                  :icon="block.sichtbar ? 'pi pi-eye' : 'pi pi-eye-slash'"
                  text
                  rounded
                  severity="secondary"
                  v-tooltip.top="block.sichtbar ? 'Ausblenden' : 'Einblenden'"
                  :aria-label="block.sichtbar ? 'Abschnitt ausblenden' : 'Abschnitt einblenden'"
                  @click="block.sichtbar = !block.sichtbar"
                />
                <Button
                  icon="pi pi-clone"
                  text
                  rounded
                  severity="secondary"
                  v-tooltip.top="'Duplizieren'"
                  aria-label="Abschnitt duplizieren"
                  @click="duplizieren(index)"
                />
                <Button
                  icon="pi pi-trash"
                  text
                  rounded
                  severity="danger"
                  v-tooltip.top="'Löschen'"
                  aria-label="Abschnitt löschen"
                  @click="loeschen(index)"
                />
              </div>
            </template>

            <AdminStartseiteAbschnitt v-model="bloecke[index]" :aktuelleKennzahlen="kennzahlen" />
          </Panel>
        </template>
      </draggable>

      <!-- Footer actions -->
      <div
        class="sticky bottom-0 z-10 flex flex-wrap justify-between gap-2 mt-4 -mx-4 -mb-4 px-4 py-3 bg-white/95 backdrop-blur border-t border-gray-200 rounded-b-lg"
      >
        <Button label="Auf Standard zurücksetzen" text severity="secondary" @click="confirmReset" />
        <div class="flex gap-2">
          <Button
            v-if="hatAenderungen"
            label="Verwerfen"
            text
            severity="secondary"
            @click="verwerfen"
          />
          <Button label="Speichern" icon="pi pi-check" :loading="isSaving" :disabled="!hatAenderungen" @click="submit" />
        </div>
      </div>
    </template>

    <Dialog
      v-model:visible="vorschauOffen"
      header="Vorschau der Startseite"
      modal
      maximizable
      dismissableMask
      class="w-full max-w-6xl"
    >
      <p class="text-xs text-gray-500 mb-3">
        Zeigt den aktuellen, noch nicht gespeicherten Stand. Buttons und Links sind in der Vorschau
        deaktiviert.
      </p>
      <StartseiteAbschnitte :bloecke="bloecke" vorschau />
    </Dialog>
  </div>
</template>

<script setup>
import { computed, nextTick, onBeforeUnmount, onMounted, reactive, ref } from 'vue'
import { onBeforeRouteLeave } from 'vue-router'
import draggable from 'vuedraggable'
import Button from 'openvue/button'
import Dialog from 'openvue/dialog'
import Menu from 'openvue/menu'
import Panel from 'openvue/panel'
import Tag from 'openvue/tag'
import { useToast } from 'openvue/usetoast'
import { useConfirm } from 'openvue/useconfirm'
import { apiClient } from '@/services/axios'
import { useEinstellungStore } from '@/stores/einstellung'
import { BLOCK_TYPEN, dupliziereBlock, parseVideoUrl, standardBloecke } from '@/utils/startseite'
import AdminStartseiteAbschnitt from './AdminStartseiteAbschnitt.vue'
import StartseiteAbschnitte from './StartseiteAbschnitte.vue'

const toast = useToast()
const confirm = useConfirm()
const einstellungStore = useEinstellungStore()

const isLoading = ref(false)
const isSaving = ref(false)
const bloecke = ref([])
const gespeicherterStand = ref('[]')
const offen = reactive(new Set())
const panelRefs = {}
const hinzufuegenMenu = ref(null)
const vorschauOffen = ref(false)
const kennzahlen = ref(null)

const hatAenderungen = computed(() => JSON.stringify(bloecke.value) !== gespeicherterStand.value)

// ---------------------------------------------------------------------------
// Loading / saving
// ---------------------------------------------------------------------------

const uebernehmen = (daten) => {
  bloecke.value = daten.startseiteBloecke ?? standardBloecke(daten)
  gespeicherterStand.value = JSON.stringify(bloecke.value)
  offen.clear()
}

const fetchEinstellung = async () => {
  isLoading.value = true
  try {
    const [einstellung, zahlen] = await Promise.all([
      apiClient.get('/admin/einstellung'),
      apiClient.get('/public/startseite/kennzahlen').catch(() => ({ data: null }))
    ])
    uebernehmen(einstellung.data)
    kennzahlen.value = zahlen.data
  } catch {
    toast.add({
      severity: 'error',
      summary: 'Fehler',
      detail: 'Startseite konnte nicht geladen werden.',
      life: 3000
    })
  } finally {
    isLoading.value = false
  }
}

onMounted(fetchEinstellung)

const speichern = async (payload, erfolgsText) => {
  isSaving.value = true
  try {
    const res = await apiClient.patch('/admin/einstellung', payload)
    uebernehmen(res.data)
    await einstellungStore.fetchEinstellung()
    toast.add({ severity: 'success', summary: erfolgsText, life: 3000 })
  } catch {
    toast.add({
      severity: 'error',
      summary: 'Fehler',
      detail: 'Startseite konnte nicht gespeichert werden.',
      life: 3000
    })
  } finally {
    isSaving.value = false
  }
}

const submit = () => speichern({ startseiteBloecke: bloecke.value }, 'Gespeichert')

const verwerfen = () => {
  bloecke.value = JSON.parse(gespeicherterStand.value)
}

const confirmReset = () => {
  confirm.require({
    message:
      'Alle Abschnitte werden gelöscht und der Standardaufbau der Startseite wird wiederhergestellt.',
    header: 'Auf Standard zurücksetzen',
    icon: 'pi pi-exclamation-triangle',
    rejectProps: { label: 'Abbrechen', severity: 'secondary', outlined: true },
    acceptProps: { label: 'Zurücksetzen', severity: 'danger' },
    accept: () =>
      speichern(
        {
          startseiteBloecke: null,
          startseiteTitel: null,
          startseiteUntertitel: null,
          startseiteInhalt: null
        },
        'Auf Standard zurückgesetzt'
      )
  })
}

// ---------------------------------------------------------------------------
// Section actions
// ---------------------------------------------------------------------------

const zeigeAbschnitt = async (id) => {
  offen.add(id)
  await nextTick()
  panelRefs[id]?.$el?.scrollIntoView({ behavior: 'smooth', block: 'start' })
}

const hinzufuegenItems = Object.values(BLOCK_TYPEN).map((def) => ({
  label: def.label,
  icon: def.icon,
  beschreibung: def.beschreibung,
  command: () => {
    const block = def.neu()
    bloecke.value.push(block)
    zeigeAbschnitt(block.id)
  }
}))

const verschieben = (index, richtung) => {
  const [block] = bloecke.value.splice(index, 1)
  bloecke.value.splice(index + richtung, 0, block)
}

const duplizieren = (index) => {
  const kopie = dupliziereBlock(bloecke.value[index])
  bloecke.value.splice(index + 1, 0, kopie)
  zeigeAbschnitt(kopie.id)
}

const loeschen = (index) => {
  const block = bloecke.value[index]
  confirm.require({
    message: `Der Abschnitt „${BLOCK_TYPEN[block.typ]?.label}${
      zusammenfassung(block) ? ` – ${zusammenfassung(block)}` : ''
    }“ wird entfernt. Die Änderung wird erst mit „Speichern“ übernommen.`,
    header: 'Abschnitt löschen',
    icon: 'pi pi-exclamation-triangle',
    rejectProps: { label: 'Abbrechen', severity: 'secondary', outlined: true },
    acceptProps: { label: 'Löschen', severity: 'danger' },
    accept: () => {
      const aktuellerIndex = bloecke.value.findIndex((b) => b.id === block.id)
      if (aktuellerIndex !== -1) bloecke.value.splice(aktuellerIndex, 1)
      offen.delete(block.id)
    }
  })
}

const umschalten = (id, auf) => (auf ? offen.add(id) : offen.delete(id))

const alleZugeklappt = computed(() => offen.size === 0)
const alleUmschalten = () => {
  if (alleZugeklappt.value) bloecke.value.forEach((b) => offen.add(b.id))
  else offen.clear()
}

const zusammenfassung = (block) => {
  switch (block.typ) {
    case 'video': {
      const video = parseVideoUrl(block.url)
      return block.titel || (video ? `${video.anbieter === 'vimeo' ? 'Vimeo' : 'YouTube'}: ${video.id}` : 'Kein gültiger Link')
    }
    case 'kacheln':
      return block.titel || `${block.kacheln?.length ?? 0} Kacheln`
    case 'kennzahlen':
      return block.titel || (block.eintraege || []).map((e) => e.label).filter(Boolean).join(', ')
    case 'faq':
      return `${block.titel ? `${block.titel} – ` : ''}${block.eintraege?.length ?? 0} Fragen`
    case 'text':
      return block.titel || block.inhalt?.replace(/<[^>]+>/g, ' ').replace(/\s+/g, ' ').trim().slice(0, 80)
    default:
      return block.titel
  }
}

// ---------------------------------------------------------------------------
// Unsaved changes protection
// ---------------------------------------------------------------------------

const beforeUnload = (event) => {
  if (hatAenderungen.value) {
    event.preventDefault()
    event.returnValue = ''
  }
}
onMounted(() => window.addEventListener('beforeunload', beforeUnload))
onBeforeUnmount(() => window.removeEventListener('beforeunload', beforeUnload))

onBeforeRouteLeave(() => {
  if (!hatAenderungen.value) return true
  return new Promise((resolve) => {
    confirm.require({
      message: 'Es gibt ungespeicherte Änderungen an der Startseite. Seite trotzdem verlassen?',
      header: 'Ungespeicherte Änderungen',
      icon: 'pi pi-exclamation-triangle',
      rejectProps: { label: 'Bleiben', severity: 'secondary', outlined: true },
      acceptProps: { label: 'Verlassen', severity: 'danger' },
      accept: () => resolve(true),
      reject: () => resolve(false),
      onHide: () => resolve(false)
    })
  })
})
</script>
