<template>
  <div>
    <div class="flex items-center justify-between gap-4">
      <BaseSubheading>Mobilitätschecks</BaseSubheading>
      <RouterLink :to="`${route.fullPath}/neu`" class="flex">
        <Button icon="pi pi-plus" label="Mobilitätscheck hinzufügen" size="small" />
      </RouterLink>
    </div>
    <MobilitaetscheckListe />
  </div>
</template>

<script setup>
import { useRoute } from 'vue-router'
import MobilitaetscheckListe from '@/components/MobilitaetscheckListe.vue'
import Button from 'openvue/button'

const route = useRoute()
</script>

<style></style>
