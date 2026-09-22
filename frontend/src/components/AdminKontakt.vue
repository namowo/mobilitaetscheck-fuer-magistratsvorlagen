<template>
  <BaseCard>
    <div class="flex items-center justify-between mb-4">
      <h5 class="text-lg font-semibold">Kontakt</h5>
    </div>
    <p class="text-sm text-gray-500 mb-4">
      Diese E-Mail-Adresse wird bei der Registrierung vorgeschlagen, wenn Nutzende eine Kommune
      anfragen möchten, die noch nicht Teil des Mobilitätschecks ist.
    </p>

    <BaseSpinner v-if="isLoading" />
    <template v-else>
      <div class="field">
        <FloatLabel variant="on">
          <InputText id="kontakt-email" v-model="kontaktEmail" class="w-full" />
          <label for="kontakt-email">Kontakt-E-Mail-Adresse</label>
        </FloatLabel>
      </div>
      <div class="flex justify-end mt-4">
        <Button label="Speichern" @click="submit" :loading="isSaving" />
      </div>
    </template>
  </BaseCard>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import Button from 'openvue/button'
import InputText from 'openvue/inputtext'
import FloatLabel from 'openvue/floatlabel'
import { apiClient } from '@/services/axios'
import { useToast } from 'openvue/usetoast'

const isLoading = ref(false)
const isSaving = ref(false)
const kontaktEmail = ref('')

const toast = useToast()

const fetchEinstellung = async () => {
  isLoading.value = true
  try {
    const res = await apiClient.get('/admin/einstellung')
    kontaktEmail.value = res.data.kontaktEmail || ''
  } catch {
    kontaktEmail.value = ''
  } finally {
    isLoading.value = false
  }
}

onMounted(fetchEinstellung)

const submit = async () => {
  isSaving.value = true
  try {
    await apiClient.patch('/admin/einstellung', {
      kontaktEmail: kontaktEmail.value || null
    })
    toast.add({ severity: 'success', summary: 'Gespeichert', life: 3000 })
  } catch {
    toast.add({
      severity: 'error',
      summary: 'Fehler',
      detail: 'Kontakt-E-Mail konnte nicht gespeichert werden.',
      life: 3000
    })
  } finally {
    isSaving.value = false
  }
}
</script>
