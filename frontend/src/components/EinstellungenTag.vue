<template>
  <div>
    <!-- Display list of submissions -->

    <Dialog
      v-model:visible="isModalOpen"
      header="Tag hinzufügen"
      modal
      dismissableMask
      class="w-full max-w-[50rem]"
    >
      <EinstellungenTagFormular :editMode="false" @add-item="onSubmit" />
    </Dialog>
    <Dialog
      v-model:visible="editMode"
      header="Tag bearbeiten"
      modal
      dismissableMask
      class="w-full max-w-[50rem]"
    >
      <EinstellungenTagFormular
        :editMode="true"
        :item="itemToEdit"
        @update-item="onUpdate"
        @delete-item="onDelete"
      />
    </Dialog>
    <div class="flex gap-4 items-center mb-2">
      <BaseSubheading>Tags</BaseSubheading>
      <Button
        v-tooltip="'Neuen Tag hinzufügen'"
        icon="pi pi-plus"
        rounded
        aria-label="Neuen Tag hinzufügen"
        data-tour="tag-neu"
        @click="toggleModal"
      />
    </div>
    <p class="text-sm text-gray-600 mb-5">
      Tags sind Schlagwörter, mit denen Sie Textbausteine und Indikatoren thematisch ordnen. Beim
      Einfügen von Textbausteinen in einen Mobilitätscheck lässt sich die Auswahl nach Tags filtern.
    </p>
    <EinstellungenSucheSortierung
      v-model:suche="suche"
      v-model:sortierung="sortierung"
      v-model:sichtbarkeit="sichtbarkeit"
      v-model:zusatz="zusatz"
      :zusatzOptionen="zusatzOptionen"
      :anzahlFilter="anzahlFilter"
      :anzahl="isLoading ? null : filteredTags.length"
      :gesamt="tags.length"
      :einheit="['Tag', 'Tags']"
      suchLabel="Nach Tag suchen"
      @zuruecksetzen="zuruecksetzen"
    />
    <BaseSkeleton v-if="isLoading" :rows="5" />
    <DataView
      v-else
      :value="filteredTags"
      dataKey="id"
      layout="grid"
      :first="first"
      class="mt-4"
      paginator
      :rows="24"
      :rowsPerPageOptions="[12, 24, 48]"
      @page="first = $event.first"
    >
      <template #grid="{ items }">
        <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-3 py-1">
          <div
            v-for="item in items"
            :key="item.id"
            :role="istAndereGemeinde(item) ? undefined : 'button'"
            :tabindex="istAndereGemeinde(item) ? undefined : 0"
            :aria-label="istAndereGemeinde(item) ? undefined : `Tag ${item.name} bearbeiten`"
            :class="[
              'group flex flex-col gap-3 rounded-xl border border-gray-200 bg-white p-4 transition',
              istAndereGemeinde(item)
                ? 'bg-gray-50'
                : 'cursor-pointer hover:border-blue-300 hover:shadow-md focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-blue-400'
            ]"
            @click="openEdit(item)"
            @keydown.enter.self="openEdit(item)"
          >
            <div class="flex items-start gap-3">
              <span
                class="flex h-9 w-9 shrink-0 items-center justify-center rounded-lg bg-blue-100 text-blue-700"
              >
                <i class="pi pi-tag" />
              </span>
              <p class="min-w-0 flex-1 font-semibold text-gray-900 break-words pt-1.5">
                {{ item.name }}
              </p>
            </div>
            <div class="flex">
              <BadgeSichtbarkeit
                :gemeindespezifisch="item.gemeindespezifisch"
                :andereGemeinde="istAndereGemeinde(item)"
              />
            </div>
          </div>
        </div>
      </template>
      <template #empty>
        <div class="flex flex-col items-center gap-2 py-10 text-gray-500">
          <i class="pi pi-tags text-2xl" />
          <span>Keine Tags gefunden.</span>
        </div>
      </template>
    </DataView>
  </div>
</template>

<script setup>
import Dialog from 'openvue/dialog'
import { computed, ref, onMounted, watch } from 'vue'
import { fetchItems, deleteItem, createItem, updateItem } from '@/composables/crud'
import EinstellungenSucheSortierung from '@/components/EinstellungenSucheSortierung.vue'
import { useSortierung } from '@/composables/sortierung'
import EinstellungenTagFormular from '@/components/EinstellungenTagFormular.vue'
import DataView from 'openvue/dataview'
import BadgeSichtbarkeit from '@/components/BadgeSichtbarkeit.vue'
import { useAuthStore } from '@/stores/auth'
import Button from 'openvue/button'

const isLoading = ref(false)
const isModalOpen = ref(false)
const tags = ref([])
const editMode = ref(false)
const itemToEdit = ref()
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

const filteredTags = computed(() => anwenden(tags.value))

// Bei geänderter Suche, Filterung oder Sortierung zur ersten Seite springen

watch(
  [suche, sortierung, sichtbarkeit, tagIds, zusatz],
  () => {
    first.value = 0
  },
  { deep: true }
)
const authStore = useAuthStore()

// Tags anderer Kommunen sind sichtbar, aber nicht bearbeitbar
const istAndereGemeinde = (tag) => tag.gemeindeId !== authStore.gemeindeId

const openEdit = (tag) => {
  if (istAndereGemeinde(tag)) return
  itemToEdit.value = tag
  editMode.value = true
}

onMounted(async () => {
  await fetchTags()
})

const toggleModal = () => {
  isModalOpen.value = !isModalOpen.value
}

const fetchTags = async () => {
  isLoading.value = true
  tags.value = await fetchItems('/einstellungen/tag')
  isLoading.value = false
}

const onDelete = async (modelId) => {
  await deleteItem({
    model: 'einstellungen/tag',
    modelId,
    detail: {
      success: 'Tag erfolgreich gelöscht',
      error: 'Fehler beim Löschen des Tags'
    }
  })
  const ix = tags.value.findIndex((tag) => tag.id === modelId)
  if (ix !== -1) {
    tags.value.splice(ix, 1)
  }
  editMode.value = false
}

const onUpdate = async ({ modelId, values }) => {
  const response = await updateItem({
    model: 'einstellungen/tag',
    modelId,
    values,
    detail: {
      success: 'Tag erfolgreich aktualisiert',
      error: 'Fehler beim Aktualisieren des Tags'
    }
  })
  const ix = tags.value.findIndex((tag) => tag.id === modelId)
  if (ix !== -1) {
    tags.value[ix] = response
  }
  editMode.value = false
}

const onSubmit = async (values) => {
  const response = await createItem({
    model: 'einstellungen/tag',
    values,
    detail: {
      success: 'Tag erfolgreich hinzugefügt',
      error: 'Fehler beim Hinzufügen des Tags'
    }
  })
  tags.value.unshift(response)
  toggleModal()
}
</script>

<style scoped>
/* Add your styling here */
</style>
