<template>
  <div class="my-5">
    <BaseSpinner v-if="isLoading" class="m-10" />
    <Tabs v-else :value="activeTab" @update:value="activeTab = $event">
      <TabList>
        <Tab v-if="isPolitik" value="meine">Meine</Tab>
        <Tab value="verwaltung">Verwaltung</Tab>
        <Tab value="politik">Politik</Tab>
      </TabList>
      <TabPanels>
        <!-- Meine (Politik only) — editable -->
        <TabPanel v-if="isPolitik" value="meine">
          <Message severity="info" :closable="false" class="mt-3 mb-3">
            Sie können einen eigenen Mobilitätscheck erstellen, indem Sie auf
            <i class="pi pi-plus mx-1" style="font-size: 0.75rem" /> klicken, oder einen
            bestehenden Mobilitätscheck aus dem Tab <strong>Verwaltung</strong> oder
            <strong>Politik</strong> duplizieren.
          </Message>
          <DataView :value="meineListe" dataKey="id">
            <template #list="slotProps">
              <MobilitaetscheckListeItem
                v-for="eingabe in slotProps.items"
                :key="eingabe.id"
                :item="eingabe"
                :readOnly="false"
                @publish-item="onPublish"
                @delete-item="onDelete"
                @export-item="onExport"
                @reload-item="refetchEingabe"
                @copy-item="onCopy"
              />
            </template>
            <template #empty>
              <p class="text-gray-500 text-sm p-4">Keine Mobilitätschecks gefunden.</p>
            </template>
          </DataView>
        </TabPanel>

        <!-- Verwaltung — editable for Verwaltung, read-only for Politik -->
        <TabPanel value="verwaltung">
          <DataView :value="verwaltungListe" dataKey="id">
            <template #list="slotProps">
              <MobilitaetscheckListeItem
                v-for="eingabe in slotProps.items"
                :key="eingabe.id"
                :item="eingabe"
                :readOnly="isPolitik"
                @publish-item="onPublish"
                @delete-item="onDelete"
                @export-item="onExport"
                @reload-item="refetchEingabe"
                @copy-item="onCopy"
              />
            </template>
            <template #empty>
              <p class="text-gray-500 text-sm p-4">Keine Mobilitätschecks gefunden.</p>
            </template>
          </DataView>
        </TabPanel>

        <!-- Politik — read-only for everyone -->
        <TabPanel value="politik">
          <DataView :value="politikListe" dataKey="id">
            <template #list="slotProps">
              <MobilitaetscheckListeItem
                v-for="eingabe in slotProps.items"
                :key="eingabe.id"
                :item="eingabe"
                :readOnly="true"
                @publish-item="onPublish"
                @delete-item="onDelete"
                @export-item="onExport"
                @reload-item="refetchEingabe"
                @copy-item="onCopy"
              />
            </template>
            <template #empty>
              <p class="text-gray-500 text-sm p-4">Keine Mobilitätschecks gefunden.</p>
            </template>
          </DataView>
        </TabPanel>
      </TabPanels>
    </Tabs>
  </div>
</template>

<script setup>
import { computed, ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { copyItem, deleteItem, exportItem, fetchItems, updateItem } from '@/composables/crud'
import MobilitaetscheckListeItem from '@/components/MobilitaetscheckListeItem.vue'
import BaseSpinner from '@/components/BaseSpinner.vue'
import DataView from 'openvue/dataview'
import Message from 'openvue/message'
import Tabs from 'openvue/tabs'
import TabList from 'openvue/tablist'
import Tab from 'openvue/tab'
import TabPanels from 'openvue/tabpanels'
import TabPanel from 'openvue/tabpanel'

const route = useRoute()
const authStore = useAuthStore()
const isLoading = ref(false)
const eingaben = ref([])

const isPolitik = computed(() => authStore.userRolleId === 2)
const activeTab = ref(authStore.userRolleId === 2 ? 'meine' : 'verwaltung')

const fetchEingaben = async () => {
  isLoading.value = true
  eingaben.value = await fetchItems(`mobilitaetscheck/eingabe/magistratsvorlage/${route.params.id}`)
  isLoading.value = false
}

const refetchEingabe = async (id) => {
  const index = eingaben.value.findIndex((e) => e.id === id)
  if (index !== -1) {
    eingaben.value[index] = await fetchItems(`mobilitaetscheck/eingabe/${id}`)
  }
}

onMounted(fetchEingaben)

// Meine: own items (Politik only)
const meineListe = computed(() =>
  eingaben.value.filter((e) => String(e.erstelltVon) === String(authStore.userId))
)

// Verwaltung: Verwaltung-role items; Politik sees only published ones
const verwaltungListe = computed(() =>
  eingaben.value.filter(
    (e) => e.autor?.rolle?.name === 'Verwaltung' && (!isPolitik.value || e.veroeffentlicht)
  )
)

// Politik: published Politik-role items excluding own
const politikListe = computed(() =>
  eingaben.value.filter(
    (e) =>
      e.autor?.rolle?.name === 'Politik' &&
      e.veroeffentlicht &&
      e.autor?.id !== authStore.userId
  )
)

const onPublish = async ({ modelId, values }) => {
  const response = await updateItem({
    model: 'mobilitaetscheck/eingabe',
    modelId,
    values,
    detail: {
      success: values.veroeffentlicht ? 'Mobilitätscheck veröffentlicht' : 'Veröffentlichung zurückgezogen',
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
