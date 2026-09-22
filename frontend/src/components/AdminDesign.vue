<template>
  <BaseCard>
    <div class="flex items-center justify-between mb-4">
      <h5 class="text-lg font-semibold">Farbschema</h5>
      <Button
        label="Auf Standard zurücksetzen"
        icon="pi pi-refresh"
        text
        severity="secondary"
        @click="confirmReset"
      />
    </div>
    <p class="text-sm text-gray-500 mb-4">
      Legen Sie die Primärfarbe der Anwendung fest. Buttons, Links und Hervorhebungen verwenden
      automatisch daraus abgeleitete Farbtöne.
    </p>

    <BaseSpinner v-if="isLoading" />
    <template v-else>
      <div class="flex flex-col gap-1">
        <label for="theme-color" class="font-semibold text-sm">Primärfarbe</label>
        <div class="flex items-center gap-3">
          <ColorPicker id="theme-color" v-model="colorPickerValue" format="hex" />
          <InputText v-model="themeColor" placeholder="#507C96" class="w-40" />
        </div>
      </div>
      <div class="flex justify-end mt-4">
        <Button label="Speichern" @click="submit" :loading="isSaving" />
      </div>
    </template>
  </BaseCard>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import Button from 'openvue/button'
import InputText from 'openvue/inputtext'
import ColorPicker from 'openvue/colorpicker'
import { apiClient } from '@/services/axios'
import { useToast } from 'openvue/usetoast'
import { useConfirm } from 'openvue/useconfirm'
import { useEinstellungStore } from '@/stores/einstellung'
import { applyThemeColor } from '@/utils/theme'

const DEFAULT_THEME_COLOR = '#507C96'

const isLoading = ref(false)
const isSaving = ref(false)
const themeColor = ref('')

const toast = useToast()
const confirm = useConfirm()
const einstellungStore = useEinstellungStore()

const colorPickerValue = computed({
  get: () => (themeColor.value || DEFAULT_THEME_COLOR).replace('#', ''),
  set: (value) => {
    themeColor.value = `#${value}`
  }
})

const fetchEinstellung = async () => {
  isLoading.value = true
  try {
    const res = await apiClient.get('/admin/einstellung')
    themeColor.value = res.data.themeColor || ''
  } catch {
    themeColor.value = ''
  } finally {
    isLoading.value = false
  }
}

onMounted(fetchEinstellung)

const HEX_COLOR_PATTERN = /^#[0-9A-Fa-f]{6}$/

const normalizeHex = (value) => {
  if (!value) return null
  const trimmed = value.trim()
  const withHash = trimmed.startsWith('#') ? trimmed : `#${trimmed}`
  return HEX_COLOR_PATTERN.test(withHash) ? withHash : null
}

const submit = async () => {
  const normalized = normalizeHex(themeColor.value)
  if (themeColor.value && !normalized) {
    toast.add({
      severity: 'error',
      summary: 'Ungültige Farbe',
      detail: "Bitte einen gültigen Hex-Farbcode angeben (z. B. '#507C96').",
      life: 4000
    })
    return
  }
  isSaving.value = true
  try {
    await apiClient.patch('/admin/einstellung', {
      themeColor: normalized
    })
    themeColor.value = normalized || ''
    toast.add({ severity: 'success', summary: 'Gespeichert', life: 3000 })
    await einstellungStore.fetchEinstellung()
    applyThemeColor(normalized || DEFAULT_THEME_COLOR)
  } catch {
    toast.add({
      severity: 'error',
      summary: 'Fehler',
      detail: 'Farbe konnte nicht gespeichert werden.',
      life: 3000
    })
  } finally {
    isSaving.value = false
  }
}

const confirmReset = () => {
  confirm.require({
    message: 'Die Primärfarbe wird zurückgesetzt und die Standardfarbe wieder verwendet.',
    header: 'Auf Standard zurücksetzen',
    icon: 'pi pi-exclamation-triangle',
    rejectProps: { label: 'Abbrechen', severity: 'secondary', outlined: true },
    acceptProps: { label: 'Zurücksetzen', severity: 'danger' },
    accept: async () => {
      themeColor.value = ''
      await submit()
    }
  })
}
</script>
