<template>{{ anzeige }}</template>

<script setup>
import { computed, ref, watch } from 'vue'
import { TransitionPresets, useTransition } from '@vueuse/core'

const props = defineProps({
  ziel: { type: Number, required: true },
  // Start counting (e.g. once visible)
  starten: { type: Boolean, default: true }
})

const reduzierteBewegung = window.matchMedia?.('(prefers-reduced-motion: reduce)').matches

const quelle = ref(0)
const aktuell = useTransition(quelle, {
  duration: reduzierteBewegung ? 0 : 1400,
  transition: TransitionPresets.easeOutCubic
})

watch(
  () => [props.starten, props.ziel],
  ([starten, ziel]) => {
    if (starten) quelle.value = ziel
  },
  { immediate: true }
)

const anzeige = computed(() => Math.round(aktuell.value).toLocaleString('de-DE'))
</script>
