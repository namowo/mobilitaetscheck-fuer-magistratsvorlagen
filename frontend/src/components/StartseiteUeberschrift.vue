<template>
  <div v-if="titel || untertitel" class="text-center max-w-3xl mx-auto mb-8 md:mb-10">
    <h2 v-if="titel" class="text-2xl md:text-3xl font-bold mb-2">{{ titel }}</h2>
    <p v-if="untertitel" class="text-base md:text-lg opacity-75">{{ untertitel }}</p>
  </div>
</template>

<script setup>
defineProps({
  titel: { type: String, default: '' },
  untertitel: { type: String, default: '' }
})
</script>
