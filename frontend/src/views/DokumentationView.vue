<template>
  <div>
    <BaseHeading>Dokumentation</BaseHeading>

    <p class="mb-6">
      Diese Seite erklärt die zentralen Konzepte des Mobilitätschecks für Magistratsvorlagen und
      richtet sich an die drei Benutzergruppen der Plattform.
    </p>

    <BaseSpinner v-if="isLoading" />
    <div v-else class="grid grid-cols-1 md:grid-cols-[220px_1fr] gap-x-8 gap-y-8">
      <nav class="md:sticky md:top-24 self-start">
        <ul class="flex flex-row md:flex-col flex-wrap gap-2">
          <li v-for="seite in seiten" :key="seite.slug">
            <a
              :href="`#${seite.slug}`"
              class="block px-3 py-1.5 rounded hover:bg-gray-100 text-sm"
              @click.prevent="scrollTo(seite.slug)"
            >
              {{ seite.titel }}
            </a>
          </li>
        </ul>
      </nav>

      <div class="min-w-0">
        <section
          v-for="(seite, index) in seiten"
          :key="seite.id"
          :id="seite.slug"
          :class="{ 'mt-10 pt-8 border-t': index > 0 }"
        >
          <div class="rich-content">
            <h2>{{ seite.titel }}</h2>
            <div v-html="seite.inhalt" />
          </div>

          <div v-if="seite.zeigtKontaktButton && kontaktEmail" class="mt-4">
            <Button
              as="a"
              :href="mailtoHref"
              label="Kontakt aufnehmen"
              icon="pi pi-envelope"
            />
          </div>
        </section>
      </div>
    </div>
  </div>
</template>

<script setup>
import { onMounted, ref } from 'vue'
import Button from 'openvue/button'
import BaseHeading from '@/components/BaseHeading.vue'
import BaseSpinner from '@/components/BaseSpinner.vue'
import { apiClient } from '@/services/axios'
import { useKommuneAnfrageMailto } from '@/composables/kommuneAnfrageMailto'

const isLoading = ref(false)
const seiten = ref([])

const { kontaktEmail, mailtoHref, fetchVorlage } = useKommuneAnfrageMailto('verwaltung')

onMounted(async () => {
  isLoading.value = true
  try {
    const res = await apiClient.get('/public/dokumentation')
    seiten.value = res.data
  } catch {
    seiten.value = []
  } finally {
    isLoading.value = false
  }
  await fetchVorlage()
})

function scrollTo(slug) {
  const el = document.getElementById(slug)
  if (el) {
    el.scrollIntoView({ behavior: 'smooth', block: 'start' })
    history.replaceState(null, '', `#${slug}`)
  }
}
</script>

<style scoped></style>
