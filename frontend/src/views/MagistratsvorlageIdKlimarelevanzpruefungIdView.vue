<template>
  <div>
    <div class="flex items-center gap-3 mb-5 [&>h1]:m-0">
      <Button
        icon="pi pi-chevron-left"
        severity="secondary"
        @click="
          router.push({
            name: 'magistratsvorlage-id-klimarelevanzpruefung',
            params: { id: route.params.id }
          })
        "
      />
      <BaseHeading>Klimacheck bearbeiten</BaseHeading>
    </div>
    <KlimarelevanzpruefungFormulare />
  </div>
</template>

<script setup>
import { useRoute, useRouter } from 'vue-router'
import Button from 'openvue/button'
import KlimarelevanzpruefungFormulare from '@/components/KlimarelevanzpruefungFormulare.vue'

const route = useRoute()
const router = useRouter()
</script>

<style></style>
