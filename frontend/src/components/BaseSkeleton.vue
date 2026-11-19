<template>
  <!-- Lade-Platzhalter in der groben Form des späteren Inhalts, damit beim Laden nichts springt. -->
  <div role="status" aria-busy="true" class="w-full">
    <span class="sr-only">Wird geladen …</span>

    <!-- Liste: gleichförmige Zeilen (Einträge, Karten untereinander) -->
    <div v-if="variant === 'list'" class="flex flex-col gap-3">
      <Skeleton v-for="i in rows" :key="i" :height="rowHeight" class="w-full" />
    </div>

    <!-- Tabelle: Kopfzeile + Zeilen mit Spalten -->
    <div v-else-if="variant === 'table'" class="flex flex-col">
      <div class="flex gap-4 px-2 py-3 border-b border-gray-200">
        <Skeleton v-for="c in columns" :key="c" height="1rem" class="flex-1" />
      </div>
      <div v-for="i in rows" :key="i" class="flex gap-4 px-2 py-3 border-b border-gray-100">
        <Skeleton v-for="c in columns" :key="c" height="1rem" class="flex-1" />
      </div>
    </div>

    <!-- Formular: Felder untereinander, Speichern-Button rechts -->
    <div v-else-if="variant === 'form'" class="flex flex-col gap-4">
      <Skeleton v-for="i in rows" :key="i" height="2.75rem" class="w-full" />
      <div class="flex justify-end">
        <Skeleton width="7rem" height="2.5rem" />
      </div>
    </div>

    <!-- Fließtext: Absätze mit unterschiedlich langen Zeilen -->
    <div v-else-if="variant === 'text'" class="flex flex-col gap-2">
      <template v-for="i in rows" :key="i">
        <Skeleton height="1rem" width="100%" />
        <Skeleton height="1rem" width="95%" />
        <Skeleton height="1rem" :width="i % 2 ? '80%' : '60%'" :class="{ 'mb-4': i < rows }" />
      </template>
    </div>

    <!-- Kacheln: Raster gleich großer Boxen -->
    <div v-else-if="variant === 'cards'" class="grid gap-4 grid-cols-2 sm:grid-cols-3 lg:grid-cols-4">
      <Skeleton v-for="i in rows" :key="i" :height="rowHeight" class="w-full" />
    </div>
  </div>
</template>

<script setup>
import Skeleton from 'openvue/skeleton'

defineProps({
  variant: {
    type: String,
    default: 'list',
    validator: (v) => ['list', 'table', 'form', 'text', 'cards'].includes(v)
  },
  rows: { type: Number, default: 4 },
  columns: { type: Number, default: 4 },
  rowHeight: { type: String, default: '3rem' }
})
</script>
