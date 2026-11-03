<template>
  <div>
    <BaseSubheading class="mb-3">Logo für PDF-Export</BaseSubheading>
    <p class="mb-5 text-sm text-gray-600">
      Das Logo Ihrer Kommune erscheint oben links in allen exportierten PDFs. Es wird automatisch
      verkleinert (maximal 45 × 14 mm, Seitenverhältnis bleibt erhalten) und überdeckt keine
      Inhalte. Ohne eigenes Logo wird das Standard-Logo verwendet. Erlaubt sind PNG und JPEG bis 2 MB.
    </p>

    <BaseSpinner v-if="isLoading" class="m-10" />
    <BaseCard v-else>
      <div class="flex flex-wrap items-center gap-6">
        <div
          class="flex h-24 w-64 items-center justify-center rounded border border-dashed border-gray-300 bg-white p-2"
        >
          <img
            v-if="previewUrl"
            :src="previewUrl"
            alt="Aktuelles Kommunen-Logo"
            class="max-h-full max-w-full object-contain"
          />
          <span v-else class="text-sm text-gray-500">Kein eigenes Logo hinterlegt</span>
        </div>
        <div class="flex gap-2">
          <input
            ref="fileInput"
            type="file"
            accept="image/png,image/jpeg"
            class="hidden"
            @change="onFileSelected"
          />
          <Button
            :label="previewUrl ? 'Logo ersetzen' : 'Logo hochladen'"
            icon="pi pi-upload"
            :loading="isUploading"
            @click="fileInput.click()"
          />
          <Button
            v-if="previewUrl"
            label="Entfernen"
            icon="pi pi-trash"
            severity="danger"
            outlined
            :disabled="isUploading"
            @click="removeLogo"
          />
        </div>
      </div>
    </BaseCard>
  </div>
</template>

<script setup>
import { onBeforeUnmount, onMounted, ref } from 'vue'
import Button from 'openvue/button'
import BaseCard from '@/components/BaseCard.vue'
import BaseSpinner from '@/components/BaseSpinner.vue'
import { apiClient } from '@/services/axios'
import { toastService } from '@/services/toast'

const API = '/einstellungen/pdf-logo'
const MAX_BYTES = 2 * 1024 * 1024

const fileInput = ref(null)
const previewUrl = ref(null)
const isLoading = ref(true)
const isUploading = ref(false)

const setPreview = (blob) => {
  if (previewUrl.value) URL.revokeObjectURL(previewUrl.value)
  previewUrl.value = blob ? URL.createObjectURL(blob) : null
}

const loadLogo = async () => {
  try {
    const response = await apiClient.get(API, { responseType: 'blob' })
    setPreview(response.data)
  } catch {
    setPreview(null) // 404 = no logo yet
  } finally {
    isLoading.value = false
  }
}

const toast = (severity, detail) => toastService.add({ severity, detail })

const onFileSelected = async (event) => {
  const file = event.target.files?.[0]
  event.target.value = '' // allow re-selecting the same file
  if (!file) return
  if (!['image/png', 'image/jpeg'].includes(file.type)) {
    toast('error', 'Nur PNG- und JPEG-Dateien sind erlaubt.')
    return
  }
  if (file.size > MAX_BYTES) {
    toast('error', 'Die Datei ist zu groß (max. 2 MB).')
    return
  }

  const formData = new FormData()
  formData.append('file', file)
  isUploading.value = true
  try {
    await apiClient.put(API, formData, { headers: { 'Content-Type': 'multipart/form-data' } })
    setPreview(file)
    toast('success', 'Logo wurde gespeichert.')
  } catch (error) {
    toast('error', error.response?.data?.detail || 'Logo konnte nicht hochgeladen werden.')
  } finally {
    isUploading.value = false
  }
}

const removeLogo = async () => {
  try {
    await apiClient.delete(API)
    setPreview(null)
    toast('success', 'Logo wurde entfernt.')
  } catch {
    toast('error', 'Logo konnte nicht entfernt werden.')
  }
}

onMounted(loadLogo)
onBeforeUnmount(() => setPreview(null))
</script>
