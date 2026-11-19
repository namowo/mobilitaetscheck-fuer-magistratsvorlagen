<template>
  <div>
    <Dialog
      v-model:visible="visible"
      modal
      dismissableMask
      header="Neues Gebiet hinzufügen"
      class="w-full max-w-[50rem]"
    >
      <EinstellungenGemeindeGebietFormular :editMode="false" @add-item="onSubmit" />
    </Dialog>
    <Dialog
      v-model:visible="editMode"
      modal
      dismissableMask
      header="Gebiet bearbeiten"
      class="w-full max-w-[50rem]"
    >
      <EinstellungenGemeindeGebietFormular
        :editMode="true"
        :item="itemToEdit"
        @update-item="onUpdate"
        @delete-item="onDelete"
      />
    </Dialog>
    <div class="flex gap-4 items-center mb-2">
      <BaseSubheading>Gebiete</BaseSubheading>
      <Button
        v-tooltip="'Neues Gebiet hinzufügen'"
        icon="pi pi-plus"
        rounded
        aria-label="Neues Gebiet hinzufügen"
        data-tour="gebiet-neu"
        @click="visible = true"
      />
    </div>
    <p class="text-sm text-gray-600 mb-5">
      Gebiete sind Stadt- oder Ortsteile Ihrer Kommune. Sie werden einmal hier gepflegt und stehen
      dann bei jeder Magistratsvorlage zur Auswahl, um ein Vorhaben räumlich einzuordnen.
    </p>
    <EinstellungenSucheSortierung
      v-model:suche="suche"
      v-model:sortierung="sortierung"
      :mitSichtbarkeit="false"
      v-model:zusatz="zusatz"
      :zusatzOptionen="zusatzOptionen"
      :anzahlFilter="anzahlFilter"
      :anzahl="isLoading ? null : filteredGebiete.length"
      :gesamt="items.length"
      :einheit="['Gebiet', 'Gebiete']"
      suchLabel="Nach Gebiet suchen"
      @zuruecksetzen="zuruecksetzen"
    />
    <BaseSkeleton v-if="isLoading" :rows="5" />
    <DataView
      v-else
      :value="filteredGebiete"
      dataKey="id"
      layout="grid"
      :first="first"
      class="mt-4"
      paginator
      :rows="24"
      :rowsPerPageOptions="[12, 24, 48]"
      @page="first = $event.first"
    >
      <template #grid="{ items: seite }">
        <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-3 py-1">
          <div
            v-for="item in seite"
            :key="item.id"
            role="button"
            tabindex="0"
            :aria-label="`Gebiet ${item.name} bearbeiten`"
            class="flex items-center gap-3 rounded-xl border border-gray-200 bg-white p-4 transition cursor-pointer hover:border-blue-300 hover:shadow-md focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-blue-400"
            @click="openEdit(item)"
            @keydown.enter.self="openEdit(item)"
          >
            <span
              class="flex h-9 w-9 shrink-0 items-center justify-center rounded-lg bg-blue-100 text-blue-700"
            >
              <i class="pi pi-map-marker" />
            </span>
            <p class="min-w-0 flex-1 font-semibold text-gray-900 break-words">{{ item.name }}</p>
          </div>
        </div>
      </template>
      <template #empty>
        <div class="flex flex-col items-center gap-2 py-10 text-gray-500">
          <i class="pi pi-map text-2xl" />
          <span>Keine Gebiete gefunden.</span>
        </div>
      </template>
    </DataView>
  </div>
</template>

<script setup>
import { computed, ref, onMounted, watch } from 'vue'
import { createItem, deleteItem, fetchItems, updateItem } from '@/composables/crud'
import Button from 'openvue/button'
import DataView from 'openvue/dataview'
import Dialog from 'openvue/dialog'
import EinstellungenGemeindeGebietFormular from '@/components/EinstellungenGemeindeGebietFormular.vue'
import EinstellungenSucheSortierung from '@/components/EinstellungenSucheSortierung.vue'
import { useSortierung } from '@/composables/sortierung'

const isLoading = ref(false)
const visible = ref(false)
const items = ref([])
const itemToEdit = ref()
const editMode = ref(false)
const first = ref(0)

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
} = useSortierung()

const filteredGebiete = computed(() => anwenden(items.value))

// Bei geänderter Suche, Filterung oder Sortierung zur ersten Seite springen

watch(
  [suche, sortierung, sichtbarkeit, tagIds, zusatz],
  () => {
    first.value = 0
  },
  { deep: true }
)

const openEdit = (item) => {
  itemToEdit.value = item
  editMode.value = true
}

onMounted(async () => {
  await fetchGebiete()
})

const fetchGebiete = async () => {
  isLoading.value = true
  items.value = await fetchItems('/einstellungen/gebiet')
  isLoading.value = false
}

const onUpdate = async ({ modelId, values }) => {
  const response = await updateItem({
    model: 'einstellungen/gebiet',
    modelId,
    values,
    detail: {
      success: 'Gebiet erfolgreich aktualisiert',
      error: 'Fehler beim Aktualisieren des Gebiets'
    }
  })
  const ix = items.value.findIndex((item) => item.id === modelId)
  if (response && ix !== -1) {
    items.value.splice(ix, 1, response)
  }
  editMode.value = false
}

const onSubmit = async (values) => {
  const response = await createItem({
    model: 'einstellungen/gebiet',
    values,
    detail: {
      success: 'Gebiet erfolgreich hinzugefügt',
      error: 'Fehler beim Hinzufügen des Gebiets'
    }
  })
  if (response) items.value.unshift(response)
  visible.value = false
}

const onDelete = async (modelId) => {
  await deleteItem({
    model: 'einstellungen/gebiet',
    modelId,
    detail: {
      success: 'Gebiet erfolgreich gelöscht',
      error: 'Fehler beim Löschen des Gebiets'
    }
  })
  const ix = items.value.findIndex((item) => item.id === modelId)
  if (ix !== -1) {
    items.value.splice(ix, 1)
  }
  editMode.value = false
}
</script>
