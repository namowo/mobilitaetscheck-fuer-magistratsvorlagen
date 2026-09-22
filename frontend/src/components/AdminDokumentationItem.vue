<template>
  <div>
    <BaseModal v-model="editMode">
      <template #header>
        <h2>Seite bearbeiten</h2>
      </template>
      <AdminDokumentationFormular :editMode="true" :item="props.item" @update-item="onUpdate" />
    </BaseModal>

    <div class="flex items-center gap-3 border border-gray-200 rounded-md p-3">
      <i class="pi pi-bars drag-handle cursor-move text-gray-400" />
      <div class="flex-1">
        <h3 class="font-semibold">{{ props.item.titel }}</h3>
        <p class="text-sm text-gray-400">#{{ props.item.slug }}</p>
      </div>
      <ButtonBearbeiten @click="toggleEditMode" noLabel />
      <ButtonLoeschen @delete-confirmed="onDelete" noLabel />
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import BaseModal from '@/components/BaseModal.vue'
import AdminDokumentationFormular from '@/components/AdminDokumentationFormular.vue'
import ButtonLoeschen from '@/components/ButtonLoeschen.vue'
import ButtonBearbeiten from '@/components/ButtonBearbeiten.vue'

const props = defineProps({
  item: Object
})

const editMode = ref(false)

const toggleEditMode = () => {
  editMode.value = !editMode.value
}

const emit = defineEmits(['delete-item', 'update-item'])

const onUpdate = (values) => {
  emit('update-item', values)
  toggleEditMode()
}

const onDelete = () => {
  emit('delete-item', props.item.id)
}
</script>

<style scoped></style>
