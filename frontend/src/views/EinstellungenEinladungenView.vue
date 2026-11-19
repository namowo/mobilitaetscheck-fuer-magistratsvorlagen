<template>
  <div>
    <div class="flex gap-4 items-center mb-2">
      <BaseSubheading>Einladungen</BaseSubheading>
    </div>
    <p class="mb-5 text-sm text-gray-600">
      Neue Benutzer treten Ihrer Kommune per Einladung bei. Wählen Sie Rolle und E-Mail-Adresse aus
      – die eingeladene Person erhält einen Link zur Registrierung, der für die gewählte Dauer
      gültig ist.
    </p>
    <EinstellungenEinladungen />
  </div>
</template>

<script setup>
import EinstellungenEinladungen from '@/components/EinstellungenEinladungen.vue'
</script>
