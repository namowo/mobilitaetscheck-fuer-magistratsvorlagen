<template>
  <div>
    <div class="flex items-center justify-between gap-4 mb-2">
      <BaseSubheading>Über das Tool</BaseSubheading>
    </div>
    <p class="text-sm text-gray-600 mb-5">
      Dieser Inhalt wird auf der öffentlichen Seite "Über das Tool" angezeigt.
    </p>

    <BaseSkeleton v-if="isLoading" :rows="1" row-height="16rem" />
    <template v-else>
      <RichContentEditor v-model="inhalt" />
      <div class="flex justify-between mt-4">
        <Button
          label="Auf Standard zurücksetzen"
          text
          severity="secondary"
          @click="confirmReset"
        />
        <Button label="Speichern" @click="submit" :loading="isSaving" />
      </div>
    </template>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import Button from 'openvue/button'
import RichContentEditor from './RichContentEditor.vue'
import { apiClient } from '@/services/axios'
import { useToast } from 'openvue/usetoast'
import { useConfirm } from 'openvue/useconfirm'
import { UEBER_DAS_TOOL_STANDARD_INHALT } from '@/utils/standardInhalte'

const isLoading = ref(false)
const isSaving = ref(false)
const inhalt = ref('')

const toast = useToast()
const confirm = useConfirm()

const fetchEinstellung = async () => {
  isLoading.value = true
  try {
    const res = await apiClient.get('/admin/einstellung')
    inhalt.value = res.data.ueberDasToolInhalt || UEBER_DAS_TOOL_STANDARD_INHALT
  } catch {
    inhalt.value = UEBER_DAS_TOOL_STANDARD_INHALT
  } finally {
    isLoading.value = false
  }
}

onMounted(fetchEinstellung)

const submit = async () => {
  isSaving.value = true
  try {
    await apiClient.patch('/admin/einstellung', {
      ueberDasToolInhalt: inhalt.value
    })
    toast.add({ severity: 'success', summary: 'Gespeichert', life: 3000 })
  } catch {
    toast.add({
      severity: 'error',
      summary: 'Fehler',
      detail: 'Inhalt konnte nicht gespeichert werden.',
      life: 3000
    })
  } finally {
    isSaving.value = false
  }
}

const confirmReset = () => {
  confirm.require({
    message: 'Der Inhalt der Seite "Über das Tool" wird gelöscht und der Standardtext wieder angezeigt.',
    header: 'Auf Standard zurücksetzen',
    icon: 'pi pi-exclamation-triangle',
    rejectProps: { label: 'Abbrechen', severity: 'secondary', outlined: true },
    acceptProps: { label: 'Zurücksetzen', severity: 'danger' },
    accept: async () => {
      inhalt.value = ''
      await submit()
    }
  })
}
</script>
