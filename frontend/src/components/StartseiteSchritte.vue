<template>
  <div class="max-w-6xl mx-auto">
    <StartseiteUeberschrift :titel="block.titel" :untertitel="block.untertitel" />

    <ol class="gestaffelt grid gap-8 md:gap-6" :class="SPALTEN_KLASSEN[Math.min(block.schritte.length, 4)]">
      <li
        v-for="(schritt, index) in block.schritte"
        :key="schritt.id"
        class="schritt relative flex md:flex-col items-start md:items-center gap-4 md:text-center"
      >
        <span
          class="relative z-10 shrink-0 flex items-center justify-center w-12 h-12 rounded-full text-lg font-bold shadow-md transition-transform duration-300 hover:scale-110"
          :class="invertiert ? 'bg-white text-[var(--p-primary-800)]' : 'bg-[var(--p-primary-600)] text-white'"
        >
          {{ index + 1 }}
        </span>
        <div>
          <h3 v-if="schritt.titel" class="text-lg font-semibold mb-1">{{ schritt.titel }}</h3>
          <p v-if="schritt.text" class="opacity-75 leading-relaxed whitespace-pre-line">{{ schritt.text }}</p>
        </div>
      </li>
    </ol>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import StartseiteUeberschrift from './StartseiteUeberschrift.vue'

const props = defineProps({ block: { type: Object, required: true } })
const invertiert = computed(() => props.block.hintergrund === 'akzent')

const SPALTEN_KLASSEN = {
  1: '',
  2: 'md:grid-cols-2',
  3: 'md:grid-cols-3',
  4: 'md:grid-cols-4'
}
</script>

<style scoped>
/* Connecting line between the numbered circles */
.schritt:not(:last-child)::before {
  content: '';
  position: absolute;
  background: currentColor;
  opacity: 0.2;
  /* mobile: vertical line below the circle */
  left: calc(1.5rem - 1px);
  top: 3.5rem;
  bottom: -1.5rem;
  width: 2px;
}
@media (min-width: 768px) {
  .schritt:not(:last-child)::before {
    /* desktop: horizontal line to the next circle */
    /* circle is 3rem wide, columns are 1.5rem apart; keep 0.5rem clear of each circle */
    left: calc(50% + 2rem);
    right: calc(-50% + 0.5rem);
    width: auto;
    top: 1.5rem;
    bottom: auto;
    height: 2px;
  }
}
</style>
