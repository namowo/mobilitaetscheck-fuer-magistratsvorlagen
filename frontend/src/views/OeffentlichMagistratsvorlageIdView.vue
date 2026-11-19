<template>
  <div class="mx-auto p-6 max-w-6xl">
    <router-link
      :to="{ name: 'oeffentlich-magistratsvorlagen', query: { gemeinde: route.query.gemeinde } }"
      class="inline-flex mb-4"
    >
      <Button
        icon="pi pi-chevron-left"
        label="zur Übersicht"
        severity="secondary"
        variant="text"
        size="small"
      />
    </router-link>

    <!-- Header -->
    <header v-if="isLoading" class="mb-6 py-2" aria-busy="true">
      <p
        class="flex items-center gap-2 text-xl font-semibold leading-tight tracking-tight text-gray-500"
      >
        Magistratsvorlage <Skeleton width="6rem" height="1.25rem" />
      </p>
      <Skeleton width="60%" height="2.25rem" class="mt-1" />
    </header>
    <header v-else-if="vorlage" class="mb-6 py-2">
      <p class="text-xl font-semibold leading-tight tracking-tight text-gray-500">
        Magistratsvorlage {{ vorlage.verwaltungsvorgangNr }}
      </p>
      <h1
        class="mt-1 mb-0 max-w-4xl text-2xl md:text-3xl font-extrabold leading-tight tracking-tight text-blue break-words hyphens-auto"
        lang="de"
      >
        {{ vorlage.name }}
      </h1>
      <div class="mt-3 flex flex-wrap items-center gap-x-4 gap-y-2 text-sm text-gray-500 dark:text-gray-400">
        <span v-if="vorlage.verwaltungsvorgangDatum" class="inline-flex items-center gap-1.5">
          <i class="pi pi-calendar text-xs" aria-hidden="true" />
          <span class="sr-only">Datum der Magistratssitzung</span>
          {{ datumFormatieren(vorlage.verwaltungsvorgangDatum) }}
        </span>
        <div
          v-if="vorlage.gemeindeGebiete?.length || vorlage.tags?.length"
          class="flex flex-wrap items-center gap-1.5"
        >
          <Tag
            v-for="g in vorlage.gemeindeGebiete"
            :key="'g' + g.id"
            :value="g.name"
            icon="pi pi-map-marker"
            severity="secondary"
            rounded
          />
          <Tag
            v-for="t in vorlage.tags"
            :key="'t' + t.id"
            :value="'#' + t.name"
            severity="info"
            rounded
          />
        </div>
      </div>
    </header>

    <!-- Not found -->
    <div
      v-if="!isLoading && !vorlage"
      class="flex flex-col items-center justify-center gap-3 py-16 text-center rounded-xl border border-dashed border-gray-300 dark:border-gray-600"
    >
      <i class="pi pi-file-excel text-4xl text-gray-300 dark:text-gray-600" />
      <div class="font-semibold">Magistratsvorlage nicht gefunden</div>
      <p class="text-sm text-gray-500 dark:text-gray-400">
        Die Vorlage existiert nicht oder ist nicht veröffentlicht.
      </p>
    </div>

    <template v-else>
      <!-- Beschreibung -->
      <section class="mb-10">
        <h2
          class="mb-2 text-xs font-semibold uppercase tracking-wider text-gray-500 dark:text-gray-400"
        >
          Beschreibung der Maßnahme
        </h2>
        <div v-if="isLoading" class="flex flex-col gap-2 max-w-3xl">
          <Skeleton width="100%" height="0.875rem" />
          <Skeleton width="95%" height="0.875rem" />
          <Skeleton width="70%" height="0.875rem" />
        </div>
        <div
          v-else-if="vorlage.beschreibung"
          class="prose prose-sm max-w-3xl text-gray-700 dark:text-gray-300"
          v-html="vorlage.beschreibung"
        ></div>
        <p v-else class="text-sm italic text-gray-500 dark:text-gray-400">
          Keine Beschreibung vorhanden.
        </p>
      </section>

      <!-- Mobilitätschecks -->
      <BaseSubheading>Mobilitätschecks</BaseSubheading>
      <Tabs v-model:value="activeTab" class="mt-2">
        <TabList>
          <Tab v-for="tab in tabs" :key="tab.value" :value="tab.value">
            <span class="inline-flex items-center gap-2">
              <i :class="tab.icon" aria-hidden="true" />
              {{ tab.label }}
              <Badge
                v-if="!isLoading"
                :value="tab.items.length"
                :severity="tab.items.length ? undefined : 'secondary'"
                size="small"
              />
            </span>
          </Tab>
        </TabList>
        <TabPanels class="px-0">
          <TabPanel v-for="tab in tabs" :key="tab.value" :value="tab.value">
            <!-- Loading -->
            <ul
              v-if="isLoading"
              class="overflow-hidden rounded-xl border border-gray-200 bg-white divide-y divide-gray-200 dark:bg-gray-800 dark:border-gray-700 dark:divide-gray-700"
            >
              <li
                v-for="i in 2"
                :key="i"
                class="flex flex-col md:flex-row md:items-center gap-4 px-5 py-4"
              >
                <div class="flex-1 flex flex-col gap-2">
                  <Skeleton width="50%" height="1.25rem" />
                  <Skeleton width="16rem" height="0.875rem" />
                </div>
                <div class="flex gap-2">
                  <Skeleton width="7rem" height="2rem" borderRadius="1rem" />
                  <Skeleton width="7rem" height="2rem" borderRadius="1rem" />
                </div>
              </li>
            </ul>

            <!-- Empty -->
            <div
              v-else-if="tab.items.length === 0"
              class="flex flex-col items-center justify-center gap-3 py-12 text-center rounded-xl border border-dashed border-gray-300 dark:border-gray-600"
            >
              <i class="pi pi-inbox text-4xl text-gray-300 dark:text-gray-600" />
              <div class="font-semibold">Keine Mobilitätschecks</div>
              <p class="text-sm text-gray-500 dark:text-gray-400">
                {{ tab.emptyText }}
              </p>
            </div>

            <!-- List -->
            <ul
              v-else
              class="overflow-hidden rounded-xl border border-gray-200 bg-white divide-y divide-gray-200 dark:bg-gray-800 dark:border-gray-700 dark:divide-gray-700"
            >
              <li v-for="check in tab.items" :key="check.id">
                <div
                  role="button"
                  tabindex="0"
                  class="check-zeile group flex flex-col md:flex-row md:items-center gap-4 px-5 py-4 cursor-pointer transition-colors hover:bg-gray-50 dark:hover:bg-gray-700/50 focus-visible:outline-none focus-visible:bg-gray-50"
                  :aria-label="`${check.name || 'Mobilitätscheck'} anzeigen`"
                  @click="openModal(check)"
                  @keydown.enter.prevent="openModal(check)"
                  @keydown.space.prevent="openModal(check)"
                >
                  <div class="flex-1 min-w-0">
                    <div
                      class="font-semibold text-base leading-snug text-gray-900 dark:text-gray-100 group-hover:text-[var(--p-primary-700)]"
                    >
                      {{ check.name || 'Kein Name' }}
                    </div>
                    <div
                      class="mt-1 flex flex-wrap items-center gap-x-4 gap-y-1 text-sm text-gray-500 dark:text-gray-400"
                    >
                      <span
                        v-if="tab.value === 'politik' && (check.autor?.vorname || check.autor?.nachname)"
                        class="inline-flex items-center gap-1.5"
                      >
                        <i class="pi pi-user text-xs" aria-hidden="true" />
                        <span class="sr-only">Erstellt von</span>
                        {{ check.autor?.vorname }} {{ check.autor?.nachname }}
                      </span>
                      <span v-if="check.autor?.gruppe?.name" class="inline-flex items-center gap-1.5">
                        <i class="pi pi-users text-xs" aria-hidden="true" />
                        <span class="sr-only">Gruppe</span>
                        {{ check.autor.gruppe.name }}
                      </span>
                      <span v-if="check.erstelltAm" class="inline-flex items-center gap-1.5">
                        <i class="pi pi-calendar text-xs" aria-hidden="true" />
                        <span class="sr-only">Erstellt am</span>
                        {{ datumFormatieren(check.erstelltAm) }}
                      </span>
                    </div>
                  </div>

                  <div
                    class="flex flex-wrap items-center gap-2 md:justify-end"
                    @click.stop
                    @keydown.stop
                  >
                    <Button
                      icon="pi pi-eye"
                      label="Anzeigen"
                      size="small"
                      rounded
                      @click="openModal(check)"
                    />
                    <span
                      v-tooltip.top="
                        exportDisabled(check)
                          ? 'Export nicht möglich: unvollständige Angaben'
                          : undefined
                      "
                    >
                      <Button
                        icon="pi pi-download"
                        label="PDF"
                        size="small"
                        severity="secondary"
                        variant="outlined"
                        rounded
                        :loading="exportingId === check.id"
                        :disabled="exportDisabled(check)"
                        @click="exportCheck(check.id)"
                      />
                    </span>
                    <i
                      class="pi pi-chevron-right hidden md:block ml-2 text-gray-300 transition-transform group-hover:translate-x-0.5 group-hover:text-gray-500"
                      aria-hidden="true"
                    />
                  </div>
                </div>
              </li>
            </ul>
          </TabPanel>
        </TabPanels>
      </Tabs>
    </template>

    <!-- View modal -->
    <Dialog v-model:visible="modalVisible" modal dismissableMask class="w-full max-w-6xl">
      <template #header>
        <h2 class="text-lg font-semibold">{{ activeCheck?.name || 'Kein Name' }} anzeigen</h2>
      </template>
      <MobilitaetscheckFormularEingabeZielOber
        v-if="activeCheck"
        :editMode="modalVisible"
        :readOnly="true"
        :item="activeCheck"
        @close-modal="modalVisible = false"
      />
    </Dialog>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { apiClient } from '@/services/axios'
import { toastService } from '@/services/toast'
import MobilitaetscheckFormularEingabeZielOber from '@/components/MobilitaetscheckFormularEingabeZielOber.vue'
import Badge from 'openvue/badge'
import Button from 'openvue/button'
import Dialog from 'openvue/dialog'
import Skeleton from 'openvue/skeleton'
import Tab from 'openvue/tab'
import TabList from 'openvue/tablist'
import TabPanel from 'openvue/tabpanel'
import TabPanels from 'openvue/tabpanels'
import Tabs from 'openvue/tabs'
import Tag from 'openvue/tag'

const route = useRoute()

const vorlage = ref(null)
const mobilitaetschecks = ref([])
const isLoading = ref(true)
const modalVisible = ref(false)
const activeCheck = ref(null)
const activeTab = ref('verwaltung')
const exportingId = ref(null)

const verwaltungChecks = computed(() =>
  mobilitaetschecks.value.filter(
    (c) => c.autor?.rolle?.name === 'Verwaltung' || c.autor?.isLocalSuperuser
  )
)
const politikChecks = computed(() =>
  mobilitaetschecks.value.filter((c) => c.autor?.rolle?.name === 'Politik')
)

const tabs = computed(() => [
  {
    value: 'verwaltung',
    label: 'Verwaltung',
    icon: 'pi pi-building',
    items: verwaltungChecks.value,
    emptyText: 'Die Verwaltung hat noch keinen Mobilitätscheck veröffentlicht.'
  },
  {
    value: 'politik',
    label: 'Politik',
    icon: 'pi pi-users',
    items: politikChecks.value,
    emptyText: 'Aus der Politik wurde noch kein Mobilitätscheck veröffentlicht.'
  }
])

onMounted(async () => {
  const id = route.params.id
  try {
    const [mvRes, checksRes] = await Promise.all([
      apiClient.get(`/public/magistratsvorlage/${id}`),
      apiClient.get(`/public/mobilitaetscheck/magistratsvorlage/${id}`)
    ])
    vorlage.value = mvRes.data
    mobilitaetschecks.value = checksRes.data
    if (verwaltungChecks.value.length === 0 && politikChecks.value.length > 0) {
      activeTab.value = 'politik'
    }
  } catch {
    vorlage.value = null
  } finally {
    isLoading.value = false
  }
})

const datumFormatieren = (datum) => {
  if (!datum) return '—'
  return new Date(datum).toLocaleDateString('de-DE', {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit'
  })
}

const exportDisabled = (check) =>
  (check.eingabeZielOber ?? []).some(
    (ober) => ober.tangiert && !(ober.eingabeZielUnter ?? []).some((unter) => unter.tangiert)
  )

const openModal = (check) => {
  activeCheck.value = check
  modalVisible.value = true
}

const exportCheck = async (id) => {
  exportingId.value = id
  try {
    const response = await apiClient.get(`/public/mobilitaetscheck/export/${id}`, {
      responseType: 'blob'
    })
    const url = window.URL.createObjectURL(new Blob([response.data], { type: 'application/pdf' }))
    const link = document.createElement('a')
    link.href = url
    link.setAttribute('download', `mobilitätscheck_${id}.pdf`)
    document.body.appendChild(link)
    link.click()
    document.body.removeChild(link)
    window.URL.revokeObjectURL(url)
    toastService.add({ severity: 'success', detail: 'Mobilitätscheck erfolgreich exportiert' })
  } catch {
    toastService.add({ severity: 'error', detail: 'Fehler beim Exportieren des Mobilitätschecks' })
  } finally {
    exportingId.value = null
  }
}
</script>

<style scoped>
.check-zeile:focus-visible {
  box-shadow: inset 3px 0 0 var(--p-primary-color);
}
:deep(.p-tabpanels) {
  padding-inline: 0;
}
</style>
