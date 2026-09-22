<template>
  <BaseModal v-model="isModalOpen">
    <template #header>
      <h2>Seite hinzufügen</h2>
    </template>
    <AdminDokumentationFormular :editMode="false" @add-item="onSubmit" />
  </BaseModal>

  <div class="flex gap-4 items-center justify-between mb-5">
    <BaseSubheading>Dokumentationsseiten</BaseSubheading>
    <Button label="Seite hinzufügen" icon="pi pi-plus" size="small" @click="toggleModal" />
  </div>
  <p class="text-sm text-gray-500 mb-4">
    Ziehen Sie die Einträge, um die Reihenfolge der öffentlichen Dokumentationsseite zu ändern.
  </p>

  <BaseSpinner v-if="isLoading" class="m-10" />
  <div v-else-if="seiten.length === 0" class="text-sm text-gray-400 text-center py-4">
    Noch keine Dokumentationsseiten vorhanden.
  </div>
  <draggable
    v-else
    :list="seiten"
    item-key="id"
    handle=".drag-handle"
    class="flex flex-col gap-2"
    @change="onReorder"
  >
    <template #item="{ element }">
      <AdminDokumentationItem
        :item="element"
        @delete-item="onDelete"
        @update-item="(values) => onUpdate({ modelId: element.id, values })"
      />
    </template>
  </draggable>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import draggable from 'vuedraggable'
import { fetchItems, deleteItem, createItem, updateItem } from '@/composables/crud'
import { apiClient } from '@/services/axios'
import { useToast } from 'openvue/usetoast'
import Button from 'openvue/button'
import AdminDokumentationFormular from '@/components/AdminDokumentationFormular.vue'
import AdminDokumentationItem from '@/components/AdminDokumentationItem.vue'
import BaseSpinner from '@/components/BaseSpinner.vue'

const MODEL = 'admin/dokumentation'

const isLoading = ref(false)
const isModalOpen = ref(false)
const seiten = ref([])
const toast = useToast()

onMounted(async () => {
  await fetchSeiten()
})

const toggleModal = () => {
  isModalOpen.value = !isModalOpen.value
}

const fetchSeiten = async () => {
  isLoading.value = true
  seiten.value = await fetchItems(`/${MODEL}`)
  isLoading.value = false
}

const onSubmit = async (values) => {
  const response = await createItem({
    model: MODEL,
    values,
    detail: {
      success: 'Seite erfolgreich hinzugefügt',
      error: 'Fehler beim Hinzufügen der Seite'
    }
  })
  if (response) {
    seiten.value.push(response)
    toggleModal()
  }
}

const onUpdate = async ({ modelId, values }) => {
  const response = await updateItem({
    model: MODEL,
    modelId,
    values,
    detail: {
      success: 'Seite erfolgreich aktualisiert',
      error: 'Fehler beim Aktualisieren der Seite'
    }
  })
  if (response) {
    const ix = seiten.value.findIndex((s) => s.id === modelId)
    if (ix !== -1) {
      seiten.value[ix] = response
    }
  }
}

const onDelete = async (modelId) => {
  await deleteItem({
    model: MODEL,
    modelId,
    detail: {
      success: 'Seite erfolgreich gelöscht',
      error: 'Fehler beim Löschen der Seite'
    }
  })
  const ix = seiten.value.findIndex((s) => s.id === modelId)
  if (ix !== -1) {
    seiten.value.splice(ix, 1)
  }
}

const onReorder = async () => {
  try {
    const reihenfolge = seiten.value.map((s, index) => ({ id: s.id, reihenfolge: index }))
    await apiClient.post(`/${MODEL}/reorder`, { reihenfolge })
  } catch {
    toast.add({
      severity: 'error',
      summary: 'Fehler',
      detail: 'Reihenfolge konnte nicht gespeichert werden.',
      life: 3000
    })
    await fetchSeiten()
  }
}
</script>

<style scoped></style>
