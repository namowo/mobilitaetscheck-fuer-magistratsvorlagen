<template>
  <Teleport to="body">
    <!-- Ring around an element while the wizard dialog is open -->
    <div
      v-if="markierung && markierungRect"
      class="wizard-ring wizard-ring--puls"
      :style="boxStyle(markierungRect)"
      aria-hidden="true"
    >
      <span v-if="markierung.label" class="wizard-ring__label" :style="labelStyle(markierungRect)">
        <i class="pi pi-arrow-up text-xs" />
        {{ markierung.label }}
      </span>
    </div>

    <!-- Spotlight after following a step's action -->
    <template v-if="spotlight && spotlightRect">
      <div class="wizard-ring wizard-ring--dimmen wizard-ring--puls" :style="boxStyle(spotlightRect)" aria-hidden="true" />
      <div
        ref="popoverEl"
        class="wizard-popover"
        :style="popoverStyle"
        role="dialog"
        aria-live="polite"
        :aria-label="spotlight.title || 'Hinweis'"
        @click.stop
      >
        <div class="flex items-start gap-2">
          <i class="pi pi-compass mt-1" style="color: rgb(var(--primary-base))" />
          <div class="flex-1">
            <div v-if="spotlight.title" class="font-semibold mb-1">{{ spotlight.title }}</div>
            <p class="text-sm text-gray-700 leading-relaxed m-0">{{ spotlight.text }}</p>
          </div>
        </div>
        <div class="flex justify-end gap-2 mt-3">
          <Button
            label="Zur Einführung"
            icon="pi pi-arrow-left"
            size="small"
            text
            severity="secondary"
            @click="zurueckZurEinfuehrung"
          />
          <Button label="Verstanden" size="small" @click="schliessen" />
        </div>
      </div>
    </template>
  </Teleport>
</template>

<script setup>
import { ref, computed, watch, nextTick, onBeforeUnmount } from 'vue'
import { useRoute } from 'vue-router'
import Button from 'openvue/button'
import { useWizardSpotlight, tourSelektor } from '@/composables/wizardSpotlight'
import { useStartWizard } from '@/composables/startWizard'

const ABSTAND = 6 // px between element and ring
const RAND = 16 // px minimum distance of the popover to the viewport edge

const route = useRoute()
const { markierung, spotlight, schliessen } = useWizardSpotlight()
const { aufklappen } = useStartWizard()

const markierungEl = ref(null)
const spotlightEl = ref(null)
const markierungRect = ref(null)
const spotlightRect = ref(null)
const popoverEl = ref(null)
const popoverHoehe = ref(140)

// ---- Finding elements -------------------------------------------------------
const istSichtbar = (el) => !!el && el.getClientRects().length > 0

const findeElement = (ziel) => {
  for (const sel of tourSelektor(ziel)) {
    const el = [...document.querySelectorAll(sel)].find(istSichtbar)
    if (el) return el
  }
  return null
}

// Pages are lazy-loaded and often show a spinner first, so poll for a while.
let suchLauf = 0
const warteAuf = async (ziel, timeoutMs = 6000) => {
  const lauf = ++suchLauf
  const start = Date.now()
  while (Date.now() - start < timeoutMs) {
    if (lauf !== suchLauf) return null
    const el = findeElement(ziel)
    if (el) return el
    await new Promise((r) => setTimeout(r, 150))
  }
  return null
}

// ---- Tracking position (layout may shift, page may scroll) -------------------
let rafId = null
const messen = () => {
  markierungRect.value = istSichtbar(markierungEl.value) ? markierungEl.value.getBoundingClientRect() : null
  spotlightRect.value = istSichtbar(spotlightEl.value) ? spotlightEl.value.getBoundingClientRect() : null
  if (popoverEl.value) popoverHoehe.value = popoverEl.value.offsetHeight
  rafId = markierungEl.value || spotlightEl.value ? requestAnimationFrame(messen) : null
}
const startMessen = () => {
  if (rafId === null) rafId = requestAnimationFrame(messen)
}

watch(
  markierung,
  async (m) => {
    markierungEl.value = null
    markierungRect.value = null
    if (!m) return
    await nextTick()
    // Ring only on elements that are already there (e.g. the menu bar)
    markierungEl.value = findeElement(m.ziel)
    startMessen()
  },
  { immediate: true }
)

let spotlightRoute = null
watch(spotlight, async (s) => {
  spotlightEl.value = null
  spotlightRect.value = null
  entferneListener()
  if (!s) return
  const el = await warteAuf(s.ziel)
  if (!el || spotlight.value !== s) {
    if (spotlight.value === s) schliessen()
    return
  }
  el.scrollIntoView({ block: 'center', behavior: 'smooth' })
  spotlightEl.value = el
  spotlightRoute = route.fullPath
  startMessen()
  // Register after the current click has finished, so it doesn't close the spotlight at once
  setTimeout(fuegeListenerHinzu, 0)
})

// Leaving the page or clicking anywhere (incl. the highlighted element) ends the spotlight
watch(
  () => route.fullPath,
  (p) => {
    if (spotlightEl.value && p !== spotlightRoute) schliessen()
  }
)

const onKlick = (e) => {
  if (popoverEl.value?.contains(e.target)) return // the popover's own buttons handle this
  schliessen()
}
const onTaste = (e) => {
  if (e.key === 'Escape') schliessen()
}
const fuegeListenerHinzu = () => {
  if (!spotlightEl.value) return
  document.addEventListener('click', onKlick, true)
  document.addEventListener('keydown', onTaste)
}
const entferneListener = () => {
  document.removeEventListener('click', onKlick, true)
  document.removeEventListener('keydown', onTaste)
}

onBeforeUnmount(() => {
  entferneListener()
  if (rafId !== null) cancelAnimationFrame(rafId)
})

const zurueckZurEinfuehrung = () => {
  schliessen()
  aufklappen()
}

// ---- Styles -----------------------------------------------------------------
const boxStyle = (r) => ({
  top: `${r.top - ABSTAND}px`,
  left: `${r.left - ABSTAND}px`,
  width: `${r.width + 2 * ABSTAND}px`,
  height: `${r.height + 2 * ABSTAND}px`
})

const labelStyle = (r) => {
  // Keep the label inside the viewport, even for elements at the right edge
  const rechtsBuendig = r.left + r.width / 2 > window.innerWidth / 2
  return rechtsBuendig ? { right: 0 } : { left: 0 }
}

const popoverStyle = computed(() => {
  const r = spotlightRect.value
  if (!r) return {}
  const vw = window.innerWidth
  const vh = window.innerHeight
  const breite = Math.min(320, vw - 2 * RAND)
  const left = Math.min(Math.max(r.left, RAND), vw - breite - RAND)
  const h = popoverHoehe.value
  let top
  if (r.bottom + ABSTAND + 12 + h <= vh - RAND) top = r.bottom + ABSTAND + 12
  else if (r.top - ABSTAND - 12 - h >= RAND) top = r.top - ABSTAND - 12 - h
  else top = vh - h - RAND // large element: pin to the bottom of the viewport
  return { top: `${top}px`, left: `${left}px`, width: `${breite}px` }
})
</script>

<style scoped>
/* Above PrimeVue's modal mask, so the ring is visible while the wizard dialog is open */
.wizard-ring {
  position: fixed;
  z-index: 2000;
  border-radius: 0.6rem;
  border: 3px solid rgb(var(--primary-base));
  pointer-events: none;
}
.wizard-ring--dimmen {
  box-shadow: 0 0 0 9999px rgba(15, 23, 42, 0.5);
}
.wizard-ring--puls::after {
  content: '';
  position: absolute;
  inset: -3px;
  border-radius: inherit;
  border: 3px solid rgb(var(--primary-base));
  animation: wizard-puls 1.6s ease-out infinite;
}
@keyframes wizard-puls {
  from {
    opacity: 0.8;
    transform: scale(1);
  }
  to {
    opacity: 0;
    transform: scale(1.25);
  }
}
.wizard-ring__label {
  position: absolute;
  top: calc(100% + 8px);
  white-space: nowrap;
  display: inline-flex;
  align-items: center;
  gap: 0.35rem;
  padding: 0.25rem 0.6rem;
  border-radius: 9999px;
  font-size: 0.8rem;
  font-weight: 600;
  color: #fff;
  background: rgb(var(--primary-base));
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.25);
}
.wizard-popover {
  position: fixed;
  z-index: 2001;
  padding: 0.9rem 1rem 0.6rem;
  border-radius: 0.6rem;
  background: #fff;
  color: #1f2937;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
}
@media (prefers-reduced-motion: reduce) {
  .wizard-ring--puls::after {
    animation: none;
  }
}
</style>
