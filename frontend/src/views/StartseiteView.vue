<template>
  <div>
    <!-- Hero -->
    <div class="max-w-5xl mx-auto pt-2 pb-10 px-4">
      <div class="text-center">
        <h1 class="text-3xl font-bold mb-3">{{ titel }}</h1>
        <p class="text-lg text-gray-600 mb-6">{{ untertitel }}</p>

        <router-link :to="{ name: 'oeffentlich-magistratsvorlagen' }" custom v-slot="{ navigate, href }">
          <span
            v-tooltip.top="
              magistratsvorlagenVorhanden
                ? undefined
                : 'Es wurden noch keine Magistratsvorlagen veröffentlicht.'
            "
          >
            <Button
              label="Magistratsvorlagen ansehen"
              icon="pi pi-arrow-right"
              iconPos="right"
              :disabled="!magistratsvorlagenVorhanden"
              :data-href="magistratsvorlagenVorhanden ? href : undefined"
              @click="magistratsvorlagenVorhanden && navigate($event)"
            />
          </span>
        </router-link>
      </div>

      <div v-if="inhalt" class="rich-content mt-8" v-html="inhalt" />
    </div>
  </div>
</template>

<script setup>
import { computed, onMounted, ref } from 'vue'
import { useEinstellungStore } from '@/stores/einstellung'
import { apiClient } from '@/services/axios'
import Button from 'openvue/button'
import { STARTSEITE_STANDARD_TITEL, STARTSEITE_STANDARD_UNTERTITEL } from '@/utils/standardInhalte'

const einstellungStore = useEinstellungStore()

const titel = computed(() => einstellungStore.einstellung.startseiteTitel || STARTSEITE_STANDARD_TITEL)
const untertitel = computed(
  () => einstellungStore.einstellung.startseiteUntertitel || STARTSEITE_STANDARD_UNTERTITEL
)
const inhalt = computed(() => einstellungStore.einstellung.startseiteInhalt || '')

const magistratsvorlagenVorhanden = ref(false)

onMounted(async () => {
  const res = await apiClient.get('/public/magistratsvorlage/vorhanden')
  magistratsvorlagenVorhanden.value = res.data.vorhanden
})
</script>
