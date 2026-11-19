<template>
  <div class="my-4">
    <Tabs :value="activeTab" @update:value="activeTab = $event">
      <TabList>
        <Tab v-for="tab in tabs" :key="tab.value" :value="tab.value">
          <span class="flex items-center gap-2">
            {{ tab.label }}
            <span
              v-if="!isLoading"
              class="min-w-5 rounded-full bg-gray-100 px-1.5 text-center text-xs font-medium leading-5 text-gray-600"
            >
              {{ tab.liste.length }}
            </span>
          </span>
        </Tab>
      </TabList>
      <TabPanels class="px-0">
        <TabPanel v-for="tab in tabs" :key="tab.value" :value="tab.value">
          <p
            v-if="tab.value === 'meine'"
            class="mb-4 flex items-start gap-2 text-sm text-gray-500"
          >
            <i class="pi pi-info-circle mt-0.5" />
            <span>
              Erstellen Sie einen eigenen Mobilitätscheck über
              <strong class="font-semibold text-gray-700">Mobilitätscheck hinzufügen</strong> oder
              duplizieren Sie einen bestehenden aus den Reitern
              <strong class="font-semibold text-gray-700">Verwaltung</strong> bzw.
              <strong class="font-semibold text-gray-700">Politik</strong>.
            </span>
          </p>

          <!-- Platzhalter in der Form der Liste, damit beim Laden nichts springt -->
          <div
            v-if="isLoading"
            class="rounded-lg border border-gray-200 bg-white shadow-sm overflow-hidden divide-y divide-gray-100"
            aria-busy="true"
          >
            <div v-for="i in 3" :key="i" class="flex items-center gap-4 px-5 py-4">
              <div class="flex-1">
                <Skeleton width="40%" height="1.1rem" class="mb-2" />
                <Skeleton width="25%" height="0.9rem" />
              </div>
              <Skeleton width="7rem" height="2rem" />
            </div>
          </div>

          <DataView
            v-else
            :value="tab.liste"
            dataKey="id"
            paginator
            :rows="20"
            :rowsPerPageOptions="[10, 20, 50]"
            class="mobilitaetscheck-liste"
          >
            <template #list="slotProps">
              <ul
                class="rounded-lg border border-gray-200 bg-white shadow-sm overflow-hidden divide-y divide-gray-100"
              >
                <MobilitaetscheckListeItem
                  v-for="eingabe in slotProps.items"
                  :key="eingabe.id"
                  :item="eingabe"
                  :readOnly="tab.readOnly"
                  @publish-item="onPublish"
                  @delete-item="onDelete"
                  @export-item="onExport"
                  @reload-item="refetchEingabe"
                  @copy-item="onCopy"
                />
              </ul>
            </template>
            <template #empty>
              <div
                class="flex flex-col items-center gap-2 rounded-lg border border-dashed border-gray-300 bg-white px-6 py-10 text-center"
              >
                <span
                  class="flex h-11 w-11 items-center justify-center rounded-full bg-gray-100 text-gray-400"
                >
                  <i class="pi pi-car" />
                </span>
                <p class="m-0 font-semibold text-gray-700">Keine Mobilitätschecks vorhanden</p>
                <p class="m-0 max-w-md text-sm text-gray-500">{{ tab.leerText }}</p>
              </div>
            </template>
          </DataView>
        </TabPanel>
      </TabPanels>
    </Tabs>
  </div>
</template>

<script setup>
import { computed, ref, onMounted, onActivated } from 'vue'
import { useRoute } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { copyItem, deleteItem, exportItem, fetchItems, updateItem } from '@/composables/crud'
import MobilitaetscheckListeItem from '@/components/MobilitaetscheckListeItem.vue'
import DataView from 'openvue/dataview'
import Skeleton from 'openvue/skeleton'
import Tabs from 'openvue/tabs'
import TabList from 'openvue/tablist'
import Tab from 'openvue/tab'
import TabPanels from 'openvue/tabpanels'
import TabPanel from 'openvue/tabpanel'

const route = useRoute()
const authStore = useAuthStore()
const isLoading = ref(false)
const eingaben = ref([])

const isPolitik = computed(() => authStore.effectiveRolleId === 2)
const activeTab = ref(authStore.effectiveRolleId === 2 ? 'meine' : 'verwaltung')

const fetchEingaben = async ({ still = false } = {}) => {
  if (!still) isLoading.value = true
  eingaben.value = await fetchItems(`mobilitaetscheck/eingabe/magistratsvorlage/${route.params.id}`)
  isLoading.value = false
}

const refetchEingabe = async (id) => {
  const index = eingaben.value.findIndex((e) => e.id === id)
  if (index !== -1) {
    eingaben.value[index] = await fetchItems(`mobilitaetscheck/eingabe/${id}`)
  }
}

onMounted(() => fetchEingaben())

// Beim Zurückkehren in den (zwischengespeicherten) Reiter still aktualisieren.
let ersteAktivierung = true
onActivated(() => {
  if (ersteAktivierung) return (ersteAktivierung = false)
  fetchEingaben({ still: true })
})

// Meine: own items (Politik only)
const meineListe = computed(() =>
  eingaben.value.filter((e) => String(e.erstelltVon) === String(authStore.userId))
)

// Verwaltung: Verwaltung-role items (or local-superuser acting as Verwaltung); Politik sees only published ones
const verwaltungListe = computed(() =>
  eingaben.value.filter(
    (e) =>
      (e.autor?.rolle?.name === 'Verwaltung' || e.autor?.isLocalSuperuser) &&
      (!isPolitik.value || e.veroeffentlicht)
  )
)

// Politik: published Politik-role items excluding own
const politikListe = computed(() =>
  eingaben.value.filter(
    (e) =>
      e.autor?.rolle?.name === 'Politik' && e.veroeffentlicht && e.autor?.id !== authStore.userId
  )
)

const tabs = computed(() => [
  ...(isPolitik.value
    ? [
        {
          value: 'meine',
          label: 'Meine',
          liste: meineListe.value,
          readOnly: false,
          leerText: 'Sie haben für diese Vorlage noch keinen eigenen Mobilitätscheck erstellt.'
        }
      ]
    : []),
  {
    value: 'verwaltung',
    label: 'Verwaltung',
    liste: verwaltungListe.value,
    readOnly: isPolitik.value,
    leerText: isPolitik.value
      ? 'Die Verwaltung hat noch keinen Mobilitätscheck veröffentlicht.'
      : 'Legen Sie über „Mobilitätscheck hinzufügen“ den ersten Mobilitätscheck an.'
  },
  {
    value: 'politik',
    label: 'Politik',
    liste: politikListe.value,
    readOnly: true,
    leerText: 'Aus der Politik wurden noch keine Mobilitätschecks veröffentlicht.'
  }
])

const onPublish = async ({ modelId, values }) => {
  const response = await updateItem({
    model: 'mobilitaetscheck/eingabe',
    modelId,
    values,
    detail: {
      success: values.veroeffentlicht
        ? 'Mobilitätscheck veröffentlicht'
        : 'Veröffentlichung zurückgezogen',
      error: 'Fehler beim Veröffentlichen des Mobilitätschecks'
    }
  })
  const index = eingaben.value.findIndex((e) => e.id === modelId)
  eingaben.value[index].veroeffentlicht = response.veroeffentlicht
}

const onDelete = async (modelId) => {
  await deleteItem({
    model: 'mobilitaetscheck/eingabe',
    modelId,
    detail: {
      success: 'Mobilitätscheck erfolgreich gelöscht',
      error: 'Fehler beim Löschen des Mobilitätschecks'
    }
  })
  const index = eingaben.value.findIndex((e) => e.id === modelId)
  eingaben.value.splice(index, 1)
}

const onExport = async (modelId) => {
  await exportItem({
    model: 'mobilitaetscheck',
    modelId,
    detail: {
      success: 'Mobilitätscheck erfolgreich exportiert',
      error: 'Fehler beim Exportieren des Mobilitätschecks'
    }
  })
}

const onCopy = async (modelId) => {
  const newItem = await copyItem({
    model: 'mobilitaetscheck',
    modelId,
    detail: {
      success: 'Mobilitätscheck erfolgreich dupliziert',
      error: 'Fehler beim Duplizieren des Mobilitätschecks'
    }
  })
  if (newItem) {
    await fetchEingaben()
    activeTab.value = isPolitik.value ? 'meine' : 'verwaltung'
  }
}
</script>

<style scoped>
.mobilitaetscheck-liste :deep(.p-dataview-content) {
  background: transparent;
}
.mobilitaetscheck-liste :deep(.p-paginator) {
  background: transparent;
  margin-top: 0.75rem;
}
</style>
