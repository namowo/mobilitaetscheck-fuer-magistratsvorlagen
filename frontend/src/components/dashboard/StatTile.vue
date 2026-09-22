<template>
  <div class="bg-white border border-gray-200 rounded-lg shadow p-4 flex items-center gap-3">
    <div class="w-10 h-10 rounded-full bg-blue-100 flex items-center justify-center shrink-0">
      <i :class="[icon, 'text-blue-600']" />
    </div>
    <div class="min-w-0">
      <div class="text-2xl font-semibold leading-tight">{{ value }}</div>
      <div class="text-sm text-gray-500 truncate">{{ label }}</div>
    </div>
  </div>
</template>

<script setup>
defineProps({
  label: { type: String, required: true },
  value: { type: [Number, String], required: true },
  icon: { type: String, default: 'pi pi-chart-bar' }
})
</script>
