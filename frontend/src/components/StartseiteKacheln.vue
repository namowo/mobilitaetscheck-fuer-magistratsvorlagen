<template>
  <div class="max-w-6xl mx-auto">
    <StartseiteUeberschrift :titel="block.titel" :untertitel="block.untertitel" />

    <div class="gestaffelt grid gap-5 md:gap-6" :class="SPALTEN_KLASSEN[block.spalten] || SPALTEN_KLASSEN[3]">
      <div
        v-for="kachel in block.kacheln"
        :key="kachel.id"
        class="kachel group flex flex-col bg-white text-gray-900 border border-gray-200 rounded-xl p-6 shadow-sm transition duration-300 hover:-translate-y-1 hover:shadow-lg hover:border-[var(--p-primary-200)]"
      >
        <span
          v-if="kachel.icon"
          class="flex items-center justify-center w-12 h-12 mb-4 rounded-full bg-[var(--p-primary-50)] text-[var(--p-primary-600)] transition-colors duration-300 group-hover:bg-[var(--p-primary-600)] group-hover:text-white"
        >
          <i :class="[kachel.icon, '!text-xl']" />
        </span>
        <h3 v-if="kachel.titel" class="text-lg font-semibold mb-2">{{ kachel.titel }}</h3>
        <p v-if="kachel.text" class="text-gray-600 leading-relaxed whitespace-pre-line">{{ kachel.text }}</p>

        <div v-if="kachel.link?.label" class="mt-auto pt-4">
          <StartseiteKachelLink :link="kachel.link" />
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import StartseiteUeberschrift from './StartseiteUeberschrift.vue'
import StartseiteKachelLink from './StartseiteKachelLink.vue'

defineProps({ block: { type: Object, required: true } })

// Literal class names so Tailwind picks them up
const SPALTEN_KLASSEN = {
  2: 'sm:grid-cols-2',
  3: 'sm:grid-cols-2 lg:grid-cols-3',
  4: 'sm:grid-cols-2 lg:grid-cols-4'
}
</script>
