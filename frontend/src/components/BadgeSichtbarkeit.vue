<template>
  <!-- Statusanzeige zur Sichtbarkeit eines Eintrags (Tag, Textbaustein, Indikator) -->
  <Tag
    v-if="andereGemeinde"
    v-tooltip.top="
      'Dieser Eintrag stammt von einer anderen Kommune. Sie können ihn verwenden, aber nicht bearbeiten.'
    "
    value="Andere Kommune"
    icon="pi pi-lock"
    severity="secondary"
    class="!text-xs !font-medium whitespace-nowrap"
  />
  <Tag
    v-else-if="!gemeindespezifisch && werte.inhalteTeilen"
    v-tooltip.top="
      'Für andere Kommunen sichtbar. Diese können den Eintrag verwenden, aber nicht bearbeiten.'
    "
    value="Sichtbar"
    icon="pi pi-globe"
    severity="success"
    class="!text-xs !font-medium whitespace-nowrap"
  />
  <Tag
    v-else
    v-tooltip.top="
      werte.inhalteTeilen
        ? 'Nur für Ihre Kommune sichtbar.'
        : 'Nur für Ihre Kommune sichtbar – das Teilen ist für Ihre Kommune deaktiviert.'
    "
    value="Privat"
    icon="pi pi-eye-slash"
    severity="secondary"
    class="!text-xs !font-medium whitespace-nowrap"
  />
</template>

<script setup>
import { onMounted } from 'vue'
import Tag from 'openvue/tag'
import { useKommuneEinstellungen } from '@/composables/kommuneEinstellungen'

const { werte, laden } = useKommuneEinstellungen()
onMounted(() => laden())

defineProps({
  gemeindespezifisch: Boolean,
  andereGemeinde: Boolean
})
</script>
