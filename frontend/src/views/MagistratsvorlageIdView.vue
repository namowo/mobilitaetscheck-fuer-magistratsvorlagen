<template>
  <div>
    <div class="grid grid-cols-8 gap-x-2 grid-flow-col">
      <div class="container col-span-2 w-fit mt-10">
        <router-link :to="{ name: 'magistratsvorlage-liste' }">
          <Button
            icon="pi pi-chevron-left"
            label="zu den Vorlagen"
            class="w-full mb-5"
            severity="secondary"
          />
        </router-link>
        <Menu :model="items" class="w-fit">
          <template #item="{ item, props }">
            <router-link v-if="item.route" v-slot="{ href, navigate }" :to="item.route" custom>
              <a
                :href="href"
                v-bind="props.action"
                :class="{ 'bg-gray-200 font-semibold rounded-md': isActive(item) }"
                :aria-current="isActive(item) ? 'page' : undefined"
                @click="navigate"
              >
                <span :class="item.icon" />
                <span class="ml-2">{{ item.label }}</span>
              </a>
            </router-link>
            <a v-else :href="item.url" :target="item.target" v-bind="props.action">
              <span :class="item.icon" />
              <span class="ml-2">{{ item.label }}</span>
            </a>
          </template>
        </Menu>
      </div>
      <div class="container col-span-6">
        <header v-if="!vorlage" class="mb-6 py-2" aria-busy="true">
          <p
            class="flex items-center gap-2 text-xl font-semibold leading-tight tracking-tight text-gray-500"
          >
            Magistratsvorlage <Skeleton width="6rem" height="1.25rem" />
          </p>
          <Skeleton width="60%" height="2.25rem" class="mt-1" />
        </header>
        <header v-else class="mb-6 py-2">
          <!-- gleiche Größe wie die Abschnittsüberschriften (BaseSubheading), nur grau -->
          <p class="text-xl font-semibold leading-tight tracking-tight text-gray-500">
            Magistratsvorlage {{ vorlage.verwaltungsvorgangNr }}
          </p>
          <h1
            class="mt-1 mb-0 max-w-4xl text-2xl md:text-3xl font-extrabold leading-tight tracking-tight text-blue break-words hyphens-auto"
            lang="de"
          >
            {{ vorlage?.name }}
          </h1>
        </header>
        <!-- Reiter bleiben beim Wechseln erhalten (kein erneutes Laden mit Platzhaltern);
             „neu“-Seiten werden bewusst nicht zwischengespeichert. -->
        <RouterView v-slot="{ Component }">
          <KeepAlive :key="route.params.id" :include="GECACHTE_REITER">
            <component :is="Component" />
          </KeepAlive>
        </RouterView>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed, ref, onMounted, provide } from 'vue'
import { fetchItem } from '@/composables/crud'
import { useRoute } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import Button from 'openvue/button'
import Menu from 'openvue/menu'
import Skeleton from 'openvue/skeleton'

const route = useRoute()
const authStore = useAuthStore()
const isPolitik = computed(() => authStore.effectiveRolleId === 2)

const vorlage = ref(null)

const GECACHTE_REITER = [
  'MagistratsvorlageIdDatenView',
  'MagistratsvorlageIdMobilitaetscheckView',
  'MagistratsvorlageIdKlimarelevanzpruefungView',
  'MagistratsvorlageIdKlimacheckView'
]

const ladeVorlage = async () => {
  vorlage.value = await fetchItem(`/magistratsvorlage/${route.params.id}`)
}

onMounted(ladeVorlage)

// Unterseiten (z. B. „Allgemeine Daten“) können den Kopf nach dem Speichern aktualisieren.
provide('ladeVorlage', ladeVorlage)

const allItems = [
  {
    label: 'Allgemeine Daten',
    route: `/magistratsvorlage/${route.params.id}/daten`,
    matches: ['daten']
  },
  {
    label: 'Mobilitätschecks',
    route: `/magistratsvorlage/${route.params.id}/mobilitaetscheck`,
    matches: ['mobilitaetscheck']
  },
  {
    label: 'Klimachecks',
    route: `/magistratsvorlage/${route.params.id}/klimarelevanzpruefung`,
    matches: ['klimarelevanzpruefung', 'klimacheck'],
    verwaltungOnly: true
  }
]

// Aktiv auch auf Unterseiten, z. B. /mobilitaetscheck/neu/:checkId → „Mobilitätschecks“
const isActive = (item) => {
  const base = `/magistratsvorlage/${route.params.id}/`
  return (item.matches ?? []).some(
    (segment) => route.path === base + segment || route.path.startsWith(`${base}${segment}/`)
  )
}

const items = computed(() =>
  allItems.filter(
    (item) => !item.verwaltungOnly || (!isPolitik.value && authStore.klimacheckAktiv)
  )
)
</script>

<style></style>
