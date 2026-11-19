<template>
  <div class="max-w-5xl mx-auto">
    <h2 v-if="block.titel" class="text-2xl md:text-3xl font-bold mb-4">{{ block.titel }}</h2>
    <div v-if="block.inhalt" class="rich-content" v-html="block.inhalt" />
    <p v-else-if="vorschau" class="text-gray-400 italic">Noch kein Text eingegeben.</p>
  </div>
</template>

<script setup>
import { inject } from 'vue'

defineProps({ block: { type: Object, required: true } })
const { vorschau } = inject('startseite', { vorschau: false })
</script>
