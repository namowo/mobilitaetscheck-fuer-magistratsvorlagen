<template>
  <BaseHeading>Wähle einen neuen Check aus</BaseHeading>
  <div class="grid grid-cols-1 gap-4 w-1/2">
    <BaseButton tag="RouterLink" to="/mobilitaetscheck/neu">Mobilitätscheck</BaseButton>
    <BaseButton v-if="authStore.klimacheckAktiv" tag="RouterLink" to="/klimarelevanzpruefung/neu"
      >Klimacheck</BaseButton
    >
  </div>
</template>

<script setup>
import { useAuthStore } from '@/stores/auth'

const authStore = useAuthStore()
</script>

<style></style>
