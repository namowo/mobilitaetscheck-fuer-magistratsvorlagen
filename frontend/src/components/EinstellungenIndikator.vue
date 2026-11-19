<template>
  <div>
    <!-- Display list of submissions -->

    <Dialog
      v-model:visible="isModalOpen"
      header="Indikator hinzufügen"
      modal
      dismissableMask
      class="w-full max-w-[50rem]"
    >
      <EinstellungenIndikatorFormular :editMode="false" :tags="tags" @add-item="onSubmit" />
    </Dialog>
    <div class="flex gap-4 items-center mb-2">
      <BaseSubheading>Indikatoren</BaseSubheading>
      <Button
        v-tooltip="'Neuen Indikator hinzufügen'"
        icon="pi pi-plus"
        rounded
        aria-label="Neuen Indikator hinzufügen"
        data-tour="indikator-neu"
        @click="toggleModal"
      />
    </div>
    <p class="text-sm text-gray-600 mb-5">
      Indikatoren sind Regelwerke, Kennwerte oder Quellen, auf die sich eine Bewertung stützt. Beim
      Ausfüllen eines Mobilitätschecks können sie jedem Unterziel zugeordnet werden, um die
      Einschätzung nachvollziehbar zu begründen. Optional lässt sich eine Quellen-URL hinterlegen.
    </p>
    <EinstellungenSucheSortierung
      v-model:suche="suche"
      v-model:sortierung="sortierung"
      v-model:sichtbarkeit="sichtbarkeit"
      v-model:tagIds="tagIds"
      :tagOptionen="tags"
      v-model:zusatz="zusatz"
      :zusatzOptionen="zusatzOptionen"
      :anzahlFilter="anzahlFilter"
      :anzahl="isLoading ? null : filteredIndikatoren.length"
      :gesamt="indikatoren.length"
      :einheit="['Indikator', 'Indikatoren']"
      suchLabel="Nach Indikator suchen"
      @zuruecksetzen="zuruecksetzen"
    />
    <BaseSkeleton v-if="isLoading" :rows="5" />
    <DataView
      v-else
      :value="filteredIndikatoren"
      dataKey="id"
      :first="first"
      class="mt-4"
      @page="first = $event.first"
      paginator
      :rows="20"
      :rowsPerPageOptions="[10, 20, 50]"
    >
      <template #list="{ items }">
        <div
          class="divide-y divide-gray-100 overflow-hidden rounded-xl border border-gray-200 bg-white"
        >
          <EinstellungenIndikatorItem
            v-for="item in items"
            :key="item.id"
            :item="item"
            :tags="tags"
            @delete-item="onDelete"
            @update-item="onUpdate"
          />
        </div>
      </template>
      <template #empty>
        <div class="flex flex-col items-center gap-2 py-10 text-gray-500">
          <i class="pi pi-chart-bar text-2xl" />
          <span>Keine Indikatoren gefunden.</span>
        </div>
      </template>
    </DataView>
  </div>
</template>

<script setup>
import Dialog from 'openvue/dialog'
import DataView from 'openvue/dataview'
import { computed, ref, onMounted, watch } from 'vue'
import { createItem, deleteItem, fetchItems, updateItem } from '@/composables/crud'
import Button from 'openvue/button'
import EinstellungenSucheSortierung from '@/components/EinstellungenSucheSortierung.vue'
import { useSortierung } from '@/composables/sortierung'
import EinstellungenIndikatorFormular from '@/components/EinstellungenIndikatorFormular.vue'
import EinstellungenIndikatorItem from '@/components/EinstellungenIndikatorItem.vue'

const isLoading = ref(false)
const isModalOpen = ref(false)
const indikatoren = ref([])
const tags = ref([])

onMounted(async () => {
  await fetchIndikatoren()
  await fetchTags()
})

const toggleModal = () => {
  isModalOpen.value = !isModalOpen.value
}

const fetchIndikatoren = async () => {
  isLoading.value = true
  indikatoren.value = await fetchItems('/einstellungen/indikator')
  isLoading.value = false
}

const fetchTags = async () => {
  tags.value = await fetchItems('/einstellungen/tag')
}

const {
  suche,
  sortierung,
  sichtbarkeit,
  tagIds,
  zusatz,
  zusatzOptionen,
  anzahlFilter,
  anwenden,
  zuruecksetzen
} = useSortierung({
  zusatzFilter: {
    mitQuelle: { label: 'Nur mit Quellen-URL', test: (item) => !!item.quelleUrl },
    ohneQuelle: { label: 'Nur ohne Quellen-URL', test: (item) => !item.quelleUrl },
    ohneTags: { label: 'Nur ohne Tags', test: (item) => !item.tags?.length }
  }
})

const filteredIndikatoren = computed(() => anwenden(indikatoren.value))

// Bei geänderter Suche, Filterung oder Sortierung zur ersten Seite springen
const first = ref(0)
watch(
  [suche, sortierung, sichtbarkeit, tagIds, zusatz],
  () => {
    first.value = 0
  },
  { deep: true }
)

const onDelete = async (modelId) => {
  await deleteItem({
    model: 'einstellungen/indikator',
    modelId,
    detail: {
      success: 'Indikator erfolgreich gelöscht',
      error: 'Fehler beim Löschen des Indikators'
    }
  })
  const ix = indikatoren.value.findIndex((indikator) => indikator.id === modelId)
  if (ix !== -1) {
    indikatoren.value.splice(ix, 1)
  }
}

const onUpdate = async ({ modelId, values }) => {
  const response = await updateItem({
    model: 'einstellungen/indikator',
    modelId,
    values,
    detail: {
      success: 'Indikator erfolgreich aktualisiert',
      error: 'Fehler beim Aktualisieren des Indikators'
    }
  })
  const ix = indikatoren.value.findIndex((indikator) => indikator.id === modelId)
  if (ix !== -1) {
    indikatoren.value.splice(ix, 1, response)
  }
}

const onSubmit = async (values) => {
  const response = await createItem({
    model: 'einstellungen/indikator',
    values,
    detail: {
      success: 'Indikator erfolgreich hinzugefügt',
      error: 'Fehler beim Hinzufügen des Indikators'
    }
  })
  indikatoren.value.unshift(response)
  toggleModal()
}
</script>

<style scoped>
/* Add your styling here */
</style>
