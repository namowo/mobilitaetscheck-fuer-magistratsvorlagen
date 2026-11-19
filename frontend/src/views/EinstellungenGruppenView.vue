<template>
  <div>
    <div class="flex gap-4 items-center mb-2">
      <BaseSubheading>Gruppen</BaseSubheading>
    </div>
    <p class="mb-5 text-sm text-gray-600">
      Gruppen bilden die Organisationsstruktur Ihrer Kommune ab, etwa Ämter in der Verwaltung oder
      Fraktionen in der Politik. Die Gruppe wird bei Mobilitätschecks neben dem Namen der
      verfassenden Person angezeigt.
    </p>
    <EinstellungenGruppen />
  </div>
</template>

<script setup>
import EinstellungenGruppen from '@/components/EinstellungenGruppen.vue'
</script>
