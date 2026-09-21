<template>
  <div>
    <div class="flex items-center gap-5">
      <BaseSubheading>Klimachecks</BaseSubheading>
      <RouterLink :to="`${route.fullPath}/neu`">
        <Button
          v-tooltip="'Klimacheck hinzufügen'"
          icon="pi pi-plus"
          rounded
          aria-label="Klimacheck hinzufügen"
        />
      </RouterLink>
    </div>
    <KlimarelevanzpruefungListe />
  </div>
</template>

<script setup>
import { useRoute } from 'vue-router'
import Button from 'openvue/button'
import KlimarelevanzpruefungListe from '@/components/KlimarelevanzpruefungListe.vue'

const route = useRoute()
</script>

<style></style>
