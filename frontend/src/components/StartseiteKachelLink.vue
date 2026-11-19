<template>
  <span v-if="vorschau" :class="KLASSEN">{{ link.label }} <i :class="pfeil" /></span>
  <router-link v-else-if="ziel.to" :to="ziel.to" :class="KLASSEN">
    {{ link.label }} <i :class="pfeil" />
  </router-link>
  <a v-else-if="ziel.href" :href="ziel.href" target="_blank" rel="noopener noreferrer" :class="KLASSEN">
    {{ link.label }} <i :class="pfeil" />
  </a>
</template>

<script setup>
import { computed, inject } from 'vue'

const props = defineProps({ link: { type: Object, required: true } })
const { vorschau } = inject('startseite', { vorschau: false })

const KLASSEN =
  'inline-flex items-center gap-2 font-semibold text-[var(--p-primary-700)] hover:underline cursor-pointer'

const ziel = computed(() => {
  if (props.link.ziel !== 'extern') return { to: { name: props.link.ziel } }
  const url = (props.link.url || '').trim()
  return url.startsWith('/') ? { to: url } : { href: url }
})

const pfeil = computed(() =>
  ziel.value.href
    ? 'pi pi-external-link !text-xs'
    : 'pi pi-arrow-right !text-xs transition-transform group-hover:translate-x-1'
)
</script>
