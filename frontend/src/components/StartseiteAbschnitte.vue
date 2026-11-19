<template>
  <div class="startseite flex flex-col gap-6 pb-10">
    <section
      v-for="block in angezeigteBloecke"
      :key="block.id"
      v-einblenden
      :class="[
        'startseite-abschnitt rounded-2xl',
        `hintergrund-${block.hintergrund || 'keiner'}`,
        istVollflaechig(block)
          ? 'overflow-hidden'
          : hatHintergrund(block)
            ? 'px-4 sm:px-8 py-8 md:py-10'
            : 'px-4 sm:px-8 py-4 md:py-6'
      ]"
    >
      <component :is="KOMPONENTEN[block.typ]" :block="block" />
    </section>

    <div
      v-if="vorschau && angezeigteBloecke.length === 0"
      class="text-center text-gray-400 py-16 border-2 border-dashed rounded-2xl"
    >
      Keine sichtbaren Abschnitte.
    </div>
  </div>
</template>

<script setup>
import { computed, onMounted, provide, ref } from 'vue'
import { apiClient } from '@/services/axios'
import { parseVideoUrl, sichtbareKennzahlen } from '@/utils/startseite'
import StartseiteHero from './StartseiteHero.vue'
import StartseiteText from './StartseiteText.vue'
import StartseiteVideo from './StartseiteVideo.vue'
import StartseiteKacheln from './StartseiteKacheln.vue'
import StartseiteKennzahlen from './StartseiteKennzahlen.vue'
import StartseiteSchritte from './StartseiteSchritte.vue'
import StartseiteFaq from './StartseiteFaq.vue'
import StartseiteAufruf from './StartseiteAufruf.vue'

const props = defineProps({
  bloecke: { type: Array, required: true },
  // Admin preview: show empty/invalid sections as hints and don't navigate away on click
  vorschau: { type: Boolean, default: false }
})

const KOMPONENTEN = {
  hero: StartseiteHero,
  text: StartseiteText,
  video: StartseiteVideo,
  kacheln: StartseiteKacheln,
  kennzahlen: StartseiteKennzahlen,
  schritte: StartseiteSchritte,
  faq: StartseiteFaq,
  aufruf: StartseiteAufruf
}

const kennzahlen = ref(null)
provide('startseite', { kennzahlen, vorschau: props.vorschau })

onMounted(async () => {
  try {
    const res = await apiClient.get('/public/startseite/kennzahlen')
    kennzahlen.value = res.data
  } catch {
    kennzahlen.value = null
  }
})

const istLeer = (block) => {
  switch (block.typ) {
    case 'text':
      return !block.titel && !block.inhalt?.replace(/<p><\/p>/g, '').trim()
    case 'video':
      return !parseVideoUrl(block.url)
    case 'kacheln':
      return !block.kacheln?.length
    case 'schritte':
      return !block.schritte?.length
    case 'faq':
      return !block.eintraege?.some((e) => e.frage)
    case 'kennzahlen':
      return sichtbareKennzahlen(block, kennzahlen.value).length === 0
    default:
      return false
  }
}

const angezeigteBloecke = computed(() =>
  props.bloecke.filter(
    (b) => KOMPONENTEN[b.typ] && b.sichtbar !== false && (props.vorschau || !istLeer(b))
  )
)

// Sections on a plain background need little padding; the gap between sections already separates them
const hatHintergrund = (block) => block.hintergrund && block.hintergrund !== 'keiner'

const istVollflaechig = (block) => block.typ === 'hero' && block.layout === 'bild-hintergrund' && block.bildUrl

// Fade sections in as they scroll into view (skipped for reduced-motion users)
const vEinblenden = {
  mounted(el) {
    if (
      typeof IntersectionObserver === 'undefined' ||
      window.matchMedia?.('(prefers-reduced-motion: reduce)').matches
    ) {
      return
    }
    el.classList.add('einblenden')
    const observer = new IntersectionObserver(
      ([eintrag]) => {
        if (eintrag.isIntersecting) {
          el.classList.add('ist-sichtbar')
          observer.disconnect()
        }
      },
      { rootMargin: '0px 0px -40px 0px' }
    )
    observer.observe(el)
    el._einblendenObserver = observer
  },
  unmounted(el) {
    el._einblendenObserver?.disconnect()
  }
}
</script>

<style>
/* Headings follow the section's text colour (white on accent / image backgrounds) */
.startseite h1,
.startseite h2,
.startseite h3 {
  color: inherit;
}

/* Section backgrounds – driven by the theme's primary palette */
.startseite .hintergrund-grau {
  background: var(--p-surface-50, #f9fafb);
}
.startseite .hintergrund-akzent-hell {
  background: var(--p-primary-50);
}
.startseite .hintergrund-akzent {
  background: linear-gradient(135deg, var(--p-primary-700), var(--p-primary-900));
  color: #fff;
}
.startseite .hintergrund-akzent .rich-content a {
  color: inherit;
  text-decoration: underline;
}

/* Scroll-in animation */
.startseite .einblenden {
  opacity: 0;
  transform: translateY(24px);
  transition:
    opacity 0.6s ease-out,
    transform 0.6s ease-out;
}
.startseite .einblenden.ist-sichtbar {
  opacity: 1;
  transform: none;
}

/* Staggered children (tiles, steps, figures) once their section is visible */
.startseite .gestaffelt > * {
  transition:
    opacity 0.5s ease-out,
    transform 0.5s ease-out;
}
.startseite .einblenden:not(.ist-sichtbar) .gestaffelt > * {
  opacity: 0;
  transform: translateY(16px);
}
.startseite .gestaffelt > :nth-child(2) {
  transition-delay: 0.1s;
}
.startseite .gestaffelt > :nth-child(3) {
  transition-delay: 0.2s;
}
.startseite .gestaffelt > :nth-child(4) {
  transition-delay: 0.3s;
}
.startseite .gestaffelt > :nth-child(n + 5) {
  transition-delay: 0.4s;
}

/* Buttons on dark (accent / image) backgrounds */
.startseite .startseite-btn-hell.p-button {
  background: #fff;
  border-color: #fff;
  color: var(--p-primary-800);
}
.startseite .startseite-btn-hell.p-button:not(:disabled):hover {
  background: var(--p-primary-50);
  border-color: var(--p-primary-50);
  color: var(--p-primary-900);
}
.startseite .startseite-btn-umriss-hell.p-button {
  background: transparent;
  border-color: rgba(255, 255, 255, 0.8);
  color: #fff;
}
.startseite .startseite-btn-umriss-hell.p-button:not(:disabled):hover {
  background: rgba(255, 255, 255, 0.12);
  border-color: #fff;
  color: #fff;
}

@media (prefers-reduced-motion: reduce) {
  .startseite *,
  .startseite *::before {
    animation: none !important;
    transition: none !important;
  }
}
</style>
