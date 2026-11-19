<template>
  <div class="max-w-3xl mx-auto text-center">
    <h2 v-if="block.titel" class="text-2xl md:text-3xl font-bold mb-3">{{ block.titel }}</h2>
    <p v-if="block.text" class="text-base md:text-lg opacity-90 mb-8 whitespace-pre-line">{{ block.text }}</p>
    <StartseiteButtons :links="block.buttons" zentriert :invertiert="invertiert" />
  </div>
</template>

<script setup>
import { computed } from 'vue'
import StartseiteButtons from './StartseiteButtons.vue'

const props = defineProps({ block: { type: Object, required: true } })
const invertiert = computed(() => props.block.hintergrund === 'akzent')
</script>
