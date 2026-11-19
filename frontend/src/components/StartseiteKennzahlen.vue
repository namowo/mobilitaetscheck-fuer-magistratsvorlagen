<template>
  <div ref="wurzel" class="max-w-5xl mx-auto">
    <StartseiteUeberschrift :titel="block.titel" />

    <div v-if="eintraege.length" class="gestaffelt flex flex-wrap justify-center gap-x-6 gap-y-10">
      <div
        v-for="eintrag in eintraege"
        :key="eintrag.id"
        class="flex flex-col items-center text-center basis-40 grow max-w-xs"
      >
        <i
          v-if="eintrag.icon"
          :class="[eintrag.icon, '!text-2xl mb-3', invertiert ? 'opacity-80' : 'text-[var(--p-primary-600)]']"
        />
        <span
          class="text-4xl md:text-5xl font-bold tabular-nums"
          :class="invertiert ? '' : 'text-[var(--p-primary-700)]'"
        >
          <StartseiteZaehler :ziel="eintrag.zahl" :starten="imBild" />{{ eintrag.suffix }}
        </span>
        <span class="mt-2 text-sm md:text-base opacity-80">{{ eintrag.label }}</span>
      </div>
    </div>
    <p v-else-if="vorschau" class="text-center text-gray-400 italic">
      Keine Kennzahlen sichtbar (Werte sind 0 oder werden noch geladen).
    </p>
  </div>
</template>

<script setup>
import { computed, inject, ref } from 'vue'
import { useIntersectionObserver } from '@vueuse/core'
import { sichtbareKennzahlen } from '@/utils/startseite'
import StartseiteUeberschrift from './StartseiteUeberschrift.vue'
import StartseiteZaehler from './StartseiteZaehler.vue'

const props = defineProps({ block: { type: Object, required: true } })
const { kennzahlen, vorschau } = inject('startseite', { kennzahlen: ref(null), vorschau: false })

const eintraege = computed(() => sichtbareKennzahlen(props.block, kennzahlen.value))
const invertiert = computed(() => props.block.hintergrund === 'akzent')

// Count up once the figures scroll into view
const wurzel = ref(null)
const imBild = ref(false)
const { stop } = useIntersectionObserver(wurzel, ([eintrag]) => {
  if (eintrag?.isIntersecting) {
    imBild.value = true
    stop()
  }
})
</script>
