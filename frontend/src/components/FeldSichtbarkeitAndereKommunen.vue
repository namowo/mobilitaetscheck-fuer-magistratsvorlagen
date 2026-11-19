<template>
  <!-- Formularfeld "Für andere Kommunen sichtbar" – Umkehrung von gemeindespezifisch -->
  <div class="flex items-center justify-between gap-4 rounded-lg border border-gray-200 px-4 py-3">
    <div>
      <label :for="inputId" class="font-medium text-gray-800">Für andere Kommunen sichtbar</label>
      <p v-if="werte.inhalteTeilen" class="text-sm text-gray-500">
        Andere Kommunen können diesen Eintrag sehen und verwenden, aber nicht bearbeiten.
      </p>
      <p v-else class="text-sm text-gray-500">
        <i class="pi pi-lock text-xs mr-1" />Ihre Kommune hat das Teilen mit anderen Kommunen
        deaktiviert. Der Eintrag bleibt privat.
      </p>
    </div>
    <ToggleSwitch
      :inputId="inputId"
      :modelValue="!gemeindespezifisch"
      :disabled="!werte.inhalteTeilen"
      @update:modelValue="(sichtbar) => (gemeindespezifisch = !sichtbar)"
    />
  </div>
</template>

<script setup>
import { onMounted } from 'vue'
import ToggleSwitch from 'openvue/toggleswitch'
import { useKommuneEinstellungen } from '@/composables/kommuneEinstellungen'

defineProps({
  inputId: {
    type: String,
    default: 'sichtbarAndereKommunen'
  }
})

const { werte, laden } = useKommuneEinstellungen()
onMounted(() => laden())

const gemeindespezifisch = defineModel({ type: Boolean, default: false })
</script>
