<template>
  <div>
    <!-- Hero -->
    <div class="max-w-5xl mx-auto pt-2 pb-10 px-4">
      <div class="text-center">
        <h1 class="text-3xl font-bold mb-3">{{ titel }}</h1>
        <p class="text-lg text-gray-600 mb-6">{{ untertitel }}</p>

        <router-link :to="{ name: 'oeffentlich-magistratsvorlagen' }">
          <Button label="Magistratsvorlagen ansehen" icon="pi pi-arrow-right" iconPos="right" />
        </router-link>
      </div>

      <div v-if="inhalt" class="rich-content mt-8" v-html="inhalt" />
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useEinstellungStore } from '@/stores/einstellung'
import Button from 'primevue/button'
import { STARTSEITE_STANDARD_TITEL, STARTSEITE_STANDARD_UNTERTITEL } from '@/utils/standardInhalte'

const einstellungStore = useEinstellungStore()

const titel = computed(() => einstellungStore.einstellung.startseiteTitel || STARTSEITE_STANDARD_TITEL)
const untertitel = computed(
  () => einstellungStore.einstellung.startseiteUntertitel || STARTSEITE_STANDARD_UNTERTITEL
)
const inhalt = computed(() => einstellungStore.einstellung.startseiteInhalt || '')
</script>
