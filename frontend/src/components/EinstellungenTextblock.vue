<template>
  <div>
    <Dialog
      v-model:visible="isModalOpen"
      header="Textbaustein hinzufügen"
      modal
      dismissableMask
      class="w-full max-w-[50rem]"
    >
      <EinstellungenTextblockFormular :editMode="false" :tags="tags" @add-item="onSubmit" />
    </Dialog>
    <div class="flex gap-4 items-center mb-2">
      <BaseSubheading>Textbausteine</BaseSubheading>
      <Button
        v-tooltip="'Neuen Textbaustein hinzufügen'"
        icon="pi pi-plus"
        rounded
        aria-label="Neuen Textbaustein hinzufügen"
        data-tour="textblock-neu"
        @click="toggleModal"
      />
    </div>
    <p class="text-sm text-gray-600 mb-5">
      Textbausteine sind wiederkehrende Formulierungen, die beim Ausfüllen eines Mobilitätschecks
      mit einem Klick in die Erläuterung eines Unterziels übernommen werden können. Über Tags lassen
      sie sich thematisch ordnen und schneller wiederfinden.
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
      :anzahl="isLoading ? null : filteredTextblocks.length"
      :gesamt="textblocks.length"
      :einheit="['Textbaustein', 'Textbausteine']"
      suchLabel="Nach Textbaustein suchen"
      @zuruecksetzen="zuruecksetzen"
    />
    <BaseSkeleton v-if="isLoading" :rows="5" />
    <DataView
      v-else
      :value="filteredTextblocks"
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
          <EinstellungenTextblockItem
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
          <i class="pi pi-align-left text-2xl" />
          <span>Keine Textbausteine gefunden.</span>
        </div>
      </template>
    </DataView>
  </div>
</template>

<script setup>
import Dialog from 'openvue/dialog'
import DataView from 'openvue/dataview'
import { computed, ref, onMounted, watch } from 'vue'
import { fetchItems, deleteItem, createItem, updateItem } from '@/composables/crud'
import EinstellungenTextblockFormular from '@/components/EinstellungenTextblockFormular.vue'
import EinstellungenTextblockItem from '@/components/EinstellungenTextblockItem.vue'
import Button from 'openvue/button'
import EinstellungenSucheSortierung from '@/components/EinstellungenSucheSortierung.vue'
import { useSortierung } from '@/composables/sortierung'
import { htmlZuText } from '@/utils/html'

const isLoading = ref(false)
const isModalOpen = ref(false)
const textblocks = ref([])
const tags = ref([])

onMounted(async () => {
  await fetchTextblocks()
  await fetchTags()
})

const toggleModal = () => {
  isModalOpen.value = !isModalOpen.value
}

const fetchTextblocks = async () => {
  isLoading.value = true
  textblocks.value = await fetchItems('/einstellungen/textblock')
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
  anzeigename: (item) => htmlZuText(item.name),
  zusatzFilter: {
    ohneTags: { label: 'Nur ohne Tags', test: (item) => !item.tags?.length }
  }
})

const filteredTextblocks = computed(() => anwenden(textblocks.value))

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
    model: 'einstellungen/textblock',
    modelId,
    detail: {
      success: 'Textbaustein erfolgreich gelöscht',
      error: 'Fehler beim Löschen des Textbausteins'
    }
  })
  const ix = textblocks.value.findIndex((item) => item.id === modelId)
  if (ix !== -1) {
    textblocks.value.splice(ix, 1)
  }
}

const onUpdate = async ({ modelId, values }) => {
  const response = await updateItem({
    model: 'einstellungen/textblock',
    modelId,
    values,
    detail: {
      success: 'Textbaustein erfolgreich aktualisiert',
      error: 'Fehler beim Aktualisieren des Textbausteins'
    }
  })
  const ix = textblocks.value.findIndex((item) => item.id === response.id)
  if (ix !== -1) {
    textblocks.value.splice(ix, 1, response)
  }
}

const onSubmit = async (values) => {
  const response = await createItem({
    model: 'einstellungen/textblock',
    values,
    detail: {
      success: 'Textbaustein erfolgreich hinzugefügt',
      error: 'Fehler beim Hinzufügen des Textbausteins'
    }
  })
  textblocks.value.unshift(response)
  toggleModal()
}
</script>

<style scoped>
/* Add your styling here */
</style>
