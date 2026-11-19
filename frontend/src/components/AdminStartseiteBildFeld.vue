<template>
  <div class="flex items-center gap-3">
    <div
      class="w-28 h-16 shrink-0 rounded-md border border-gray-200 bg-gray-50 flex items-center justify-center overflow-hidden"
    >
      <img v-if="bildUrl" :src="bildUrl" alt="" class="w-full h-full object-cover" />
      <i v-else class="pi pi-image text-gray-300 !text-2xl" />
    </div>
    <div class="flex flex-wrap gap-2">
      <Button
        :label="bildUrl ? 'Anderes Bild' : 'Bild auswählen'"
        icon="pi pi-images"
        size="small"
        outlined
        @click="pickerVisible = true"
      />
      <Button
        v-if="bildUrl"
        label="Entfernen"
        icon="pi pi-times"
        size="small"
        text
        severity="secondary"
        @click="bildUrl = ''"
      />
    </div>
    <BrandingAssetPicker v-model:visible="pickerVisible" @select="auswaehlen" />
  </div>
</template>

<script setup>
import { ref } from 'vue'
import Button from 'openvue/button'
import BrandingAssetPicker from './BrandingAssetPicker.vue'

const bildUrl = defineModel({ type: String, default: '' })
const pickerVisible = ref(false)

const auswaehlen = (asset) => {
  bildUrl.value = asset.url
  pickerVisible.value = false
}
</script>
