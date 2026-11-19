<template>
  <StartseiteAbschnitte :bloecke="bloecke" class="pt-2" />
</template>

<script setup>
import { computed } from 'vue'
import { useEinstellungStore } from '@/stores/einstellung'
import { standardBloecke } from '@/utils/startseite'
import StartseiteAbschnitte from '@/components/StartseiteAbschnitte.vue'

const einstellungStore = useEinstellungStore()

// NULL = never customised → default layout (carrying over older Titel/Untertitel/Text settings)
const bloecke = computed(
  () => einstellungStore.einstellung.startseiteBloecke ?? standardBloecke(einstellungStore.einstellung)
)
</script>
