<template>
  <!-- Image as full background -->
  <div
    v-if="layout === 'bild-hintergrund'"
    class="hero relative bg-cover bg-center text-white"
    :style="{ backgroundImage: `url('${block.bildUrl}')` }"
  >
    <div class="absolute inset-0 bg-gradient-to-t from-black/80 via-black/60 to-black/45" />
    <div class="relative px-4 sm:px-8 py-20 md:py-32 text-center max-w-3xl mx-auto">
      <h1 class="hero-einstieg text-3xl md:text-5xl font-bold mb-4 drop-shadow">{{ block.titel }}</h1>
      <p v-if="block.untertitel" class="hero-einstieg hero-verzoegert-1 text-lg md:text-xl mb-8 opacity-90">
        {{ block.untertitel }}
      </p>
      <StartseiteButtons class="hero-einstieg hero-verzoegert-2" :links="block.buttons" zentriert invertiert />
    </div>
  </div>

  <!-- Text left, image right -->
  <div
    v-else-if="layout === 'bild-rechts'"
    class="hero grid gap-8 md:gap-12 md:grid-cols-2 items-center max-w-5xl mx-auto"
  >
    <div class="text-center md:text-left">
      <h1 class="hero-einstieg text-3xl md:text-5xl font-bold mb-4">{{ block.titel }}</h1>
      <p v-if="block.untertitel" class="hero-einstieg hero-verzoegert-1 text-lg md:text-xl mb-8 opacity-75">
        {{ block.untertitel }}
      </p>
      <StartseiteButtons
        class="hero-einstieg hero-verzoegert-2 justify-center md:justify-start"
        :links="block.buttons"
        :invertiert="invertiert"
      />
    </div>
    <img
      :src="block.bildUrl"
      alt=""
      class="hero-einstieg hero-verzoegert-1 w-full max-h-96 object-cover rounded-2xl shadow-xl"
    />
  </div>

  <!-- Centered (default) -->
  <div v-else class="hero text-center max-w-3xl mx-auto">
    <h1 class="hero-einstieg text-3xl md:text-5xl font-bold mb-4">{{ block.titel }}</h1>
    <p v-if="block.untertitel" class="hero-einstieg hero-verzoegert-1 text-lg md:text-xl mb-8 opacity-75">
      {{ block.untertitel }}
    </p>
    <StartseiteButtons
      class="hero-einstieg hero-verzoegert-2"
      :links="block.buttons"
      zentriert
      :invertiert="invertiert"
    />
    <img
      v-if="block.bildUrl"
      :src="block.bildUrl"
      alt=""
      class="hero-einstieg hero-verzoegert-2 mt-10 mx-auto w-full max-h-96 object-cover rounded-2xl shadow-xl"
    />
  </div>
</template>

<script setup>
import { computed } from 'vue'
import StartseiteButtons from './StartseiteButtons.vue'

const props = defineProps({ block: { type: Object, required: true } })

// Image layouts fall back to "centered" until an image is chosen
const layout = computed(() => (props.block.bildUrl ? props.block.layout || 'zentriert' : 'zentriert'))
const invertiert = computed(() => props.block.hintergrund === 'akzent')
</script>

<style scoped>
.hero-einstieg {
  animation: hero-einstieg 0.7s ease-out both;
}
.hero-verzoegert-1 {
  animation-delay: 0.12s;
}
.hero-verzoegert-2 {
  animation-delay: 0.24s;
}
@keyframes hero-einstieg {
  from {
    opacity: 0;
    transform: translateY(16px);
  }
  to {
    opacity: 1;
    transform: none;
  }
}
@media (prefers-reduced-motion: reduce) {
  .hero-einstieg {
    animation: none;
  }
}
</style>
