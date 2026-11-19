<template>
  <div class="flex flex-col gap-1">
    <label v-if="label" :for="feldId" class="font-semibold text-sm">
      {{ label }} <LabelOptional v-if="optional" />
    </label>
    <slot />
    <small v-if="hinweis" class="text-gray-500">{{ hinweis }}</small>
  </div>
</template>

<script setup>
defineProps({
  label: { type: String, default: '' },
  feldId: { type: String, default: undefined },
  optional: { type: Boolean, default: false },
  hinweis: { type: String, default: '' }
})
</script>
