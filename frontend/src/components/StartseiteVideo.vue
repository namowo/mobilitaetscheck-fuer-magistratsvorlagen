<template>
  <div :class="hochformat ? 'max-w-sm mx-auto' : 'max-w-4xl mx-auto'">
    <StartseiteUeberschrift :titel="block.titel" :untertitel="block.text" />

    <div
      v-if="!video"
      class="flex items-center justify-center text-center text-gray-400 border-2 border-dashed rounded-xl p-8"
      :style="{ aspectRatio }"
    >
      Bitte einen gültigen YouTube- oder Vimeo-Link eingeben.
    </div>

    <figure v-else>
      <div
        class="relative w-full overflow-hidden rounded-xl bg-gray-900 shadow-xl"
        :style="{ aspectRatio }"
      >
        <iframe
          v-if="geladen"
          :src="iframeUrl"
          :title="block.titel || `${anbieter.name}-Video`"
          class="absolute inset-0 w-full h-full border-0"
          allow="autoplay; encrypted-media; fullscreen; picture-in-picture"
          allowfullscreen
          referrerpolicy="strict-origin-when-cross-origin"
        />

        <!-- Two-click consent placeholder: nothing is requested from the provider before the click -->
        <div
          v-else
          class="absolute inset-0 bg-cover bg-center"
          :style="block.vorschaubildUrl ? { backgroundImage: `url('${block.vorschaubildUrl}')` } : {}"
        >
          <div
            class="absolute inset-0 flex flex-col items-center justify-center gap-4 p-4 sm:p-8 text-center text-white"
            :class="
              block.vorschaubildUrl
                ? 'bg-black/60'
                : 'bg-gradient-to-br from-[var(--p-primary-700)] to-[var(--p-primary-950)]'
            "
          >
            <button
              type="button"
              class="abspielen group flex items-center justify-center w-16 h-16 sm:w-20 sm:h-20 rounded-full bg-white/95 text-[var(--p-primary-700)] shadow-lg transition-transform hover:scale-110 focus-visible:outline focus-visible:outline-4 focus-visible:outline-white/60"
              :aria-label="`Video laden und abspielen (${anbieter.name})`"
              @click="laden"
            >
              <i class="pi pi-play !text-2xl sm:!text-3xl ml-1" />
            </button>
            <p class="text-xs sm:text-sm max-w-md leading-relaxed">
              Mit dem Abspielen werden Daten (u. a. Ihre IP-Adresse) an
              {{ anbieter.datenempfaenger }} übertragen.
              <a
                v-if="datenschutzLink.href"
                :href="datenschutzLink.href"
                target="_blank"
                rel="noopener noreferrer"
                class="underline"
                >Datenschutzerklärung</a
              >
              <router-link v-else :to="datenschutzLink.to" class="underline">Datenschutzerklärung</router-link>
            </p>
            <label class="hidden sm:flex items-center gap-2 text-xs opacity-90 cursor-pointer">
              <Checkbox v-model="immerLaden" binary :inputId="`video-immer-${block.id}`" />
              {{ anbieter.name }}-Videos künftig immer laden
            </label>
          </div>
        </div>
      </div>
      <figcaption v-if="block.bildunterschrift" class="text-sm opacity-75 mt-3 text-center">
        {{ block.bildunterschrift }}
      </figcaption>
    </figure>
  </div>
</template>

<script setup>
import { computed, ref, watch } from 'vue'
import Checkbox from 'openvue/checkbox'
import { useEinstellungStore } from '@/stores/einstellung'
import { parseVideoUrl, VIDEO_ANBIETER } from '@/utils/startseite'
import StartseiteUeberschrift from './StartseiteUeberschrift.vue'

const props = defineProps({ block: { type: Object, required: true } })

const einstellungStore = useEinstellungStore()

const SEITENVERHAELTNISSE = { '16:9': '16 / 9', '4:3': '4 / 3', '9:16': '9 / 16' }
const aspectRatio = computed(() => SEITENVERHAELTNISSE[props.block.seitenverhaeltnis] || '16 / 9')
const hochformat = computed(() => props.block.seitenverhaeltnis === '9:16')

const video = computed(() => parseVideoUrl(props.block.url))
const anbieter = computed(() => VIDEO_ANBIETER[video.value?.anbieter] || VIDEO_ANBIETER.youtube)

// Per-browser "always load videos from <provider>" choice
const speicherSchluessel = computed(() => `videoZustimmung:${video.value?.anbieter}`)
const immerLaden = ref(false)
const gespeicherteZustimmung = ref(false)
const geklickt = ref(false)

// Reset when the video changes (relevant in the admin preview)
watch(
  () => props.block.url,
  () => {
    geklickt.value = false
    try {
      gespeicherteZustimmung.value =
        !!video.value && localStorage.getItem(speicherSchluessel.value) === 'ja'
    } catch {
      gespeicherteZustimmung.value = false
    }
  },
  { immediate: true }
)

const geladen = computed(() => geklickt.value || gespeicherteZustimmung.value)

// Autoplay only after an explicit click, never on page load
const iframeUrl = computed(() => {
  if (!video.value) return ''
  return geklickt.value ? `${video.value.embedUrl}&autoplay=1` : video.value.embedUrl
})

const laden = () => {
  if (immerLaden.value) {
    try {
      localStorage.setItem(speicherSchluessel.value, 'ja')
    } catch {
      // localStorage unavailable – consent applies to this view only
    }
  }
  geklickt.value = true
}

const datenschutzLink = computed(() => {
  const e = einstellungStore.einstellung
  return e.datenschutzModus === 'url' && e.datenschutzUrl
    ? { href: e.datenschutzUrl }
    : { to: { name: 'datenschutzerklaerung' } }
})
</script>
