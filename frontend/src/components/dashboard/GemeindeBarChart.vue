<template>
  <div v-if="!data || data.length === 0" class="text-gray-400 text-sm py-6 text-center">
    Keine Daten vorhanden.
  </div>
  <div v-else class="flex flex-col gap-2 max-h-64 overflow-y-auto pr-1">
    <div v-for="row in data" :key="row.gemeinde" class="flex items-center gap-2">
      <div class="w-28 text-sm text-gray-600 truncate shrink-0" :title="row.gemeinde">
        {{ row.gemeinde }}
      </div>
      <div class="flex-1 bg-gray-100 rounded h-4 overflow-hidden">
        <div
          class="h-full bg-blue-500 rounded"
          :style="{ width: barWidth(row.anzahl) }"
        />
      </div>
      <div class="w-8 text-sm text-gray-700 text-right shrink-0">{{ row.anzahl }}</div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  data: { type: Array, default: () => [] }
})

const max = computed(() => Math.max(1, ...props.data.map((d) => d.anzahl)))

const barWidth = (value) => `${Math.max(2, (value / max.value) * 100)}%`
</script>
