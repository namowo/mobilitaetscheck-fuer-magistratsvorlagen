<template>
  <BaseCard>
    <div class="flex items-center justify-between mb-4">
      <h5 class="text-lg font-semibold">Startseite</h5>
    </div>
    <p class="text-sm text-gray-500 mb-4">
      Dieser Inhalt ersetzt den Hero-Bereich (Titel, Untertitel und Text) auf der Startseite. Die
      Kommunenauswahl und Liste der Magistratsvorlagen sind auf einer eigenen Unterseite
      erreichbar. Leer lassen, um den Standardtext anzuzeigen.
    </p>

    <BaseSpinner v-if="isLoading" />
    <template v-else>
      <div class="flex flex-col gap-4">
        <div class="flex flex-col gap-1">
          <label for="startseite-titel" class="font-semibold text-sm">Titel</label>
          <InputText
            id="startseite-titel"
            v-model="titel"
            :placeholder="STARTSEITE_STANDARD_TITEL"
          />
        </div>
        <div class="flex flex-col gap-1">
          <label for="startseite-untertitel" class="font-semibold text-sm">Untertitel</label>
          <InputText
            id="startseite-untertitel"
            v-model="untertitel"
            :placeholder="STARTSEITE_STANDARD_UNTERTITEL"
          />
        </div>
        <div class="flex flex-col gap-1">
          <label class="font-semibold text-sm">Text</label>
          <RichContentEditor v-model="inhalt" />
        </div>
      </div>
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
  </BaseCard>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import Button from 'primevue/button'
import InputText from 'primevue/inputtext'
import { apiClient } from '@/services/axios'
import { useToast } from 'primevue/usetoast'
import { useConfirm } from 'primevue/useconfirm'
import RichContentEditor from './RichContentEditor.vue'
import { STARTSEITE_STANDARD_TITEL, STARTSEITE_STANDARD_UNTERTITEL } from '@/utils/standardInhalte'

const isLoading = ref(false)
const isSaving = ref(false)
const titel = ref('')
const untertitel = ref('')
const inhalt = ref('')

const toast = useToast()
const confirm = useConfirm()

const fetchEinstellung = async () => {
  isLoading.value = true
  try {
    const res = await apiClient.get('/admin/einstellung')
    titel.value = res.data.startseiteTitel || ''
    untertitel.value = res.data.startseiteUntertitel || ''
    inhalt.value = res.data.startseiteInhalt || ''
  } catch {
    titel.value = ''
    untertitel.value = ''
    inhalt.value = ''
  } finally {
    isLoading.value = false
  }
}

onMounted(fetchEinstellung)

const submit = async () => {
  isSaving.value = true
  try {
    await apiClient.patch('/admin/einstellung', {
      startseiteTitel: titel.value,
      startseiteUntertitel: untertitel.value,
      startseiteInhalt: inhalt.value
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
    message: 'Der Startseiten-Inhalt wird gelöscht und der Standardtext wieder angezeigt.',
    header: 'Auf Standard zurücksetzen',
    icon: 'pi pi-exclamation-triangle',
    rejectProps: { label: 'Abbrechen', severity: 'secondary', outlined: true },
    acceptProps: { label: 'Zurücksetzen', severity: 'danger' },
    accept: async () => {
      titel.value = ''
      untertitel.value = ''
      inhalt.value = ''
      await submit()
    }
  })
}
</script>
