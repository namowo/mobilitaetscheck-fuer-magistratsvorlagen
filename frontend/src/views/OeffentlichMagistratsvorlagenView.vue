<template>
  <div class="mx-auto p-6">
    <div class="flex flex-col md:flex-row md:items-center gap-3 md:gap-5 mb-4">
      <BaseHeading class="mb-0">Veröffentlichte Magistratsvorlagen</BaseHeading>
      <Select
        v-if="selectedGemeindeId !== null"
        v-model="selectedGemeindeId"
        :options="gemeinden"
        optionLabel="name"
        optionValue="id"
        placeholder="Kommune auswählen"
        aria-label="Kommune auswählen"
        class="w-full md:w-72 md:ml-auto"
        :loading="isLoadingGemeinden"
        filter
        filterPlaceholder="Suchen..."
        @change="onGemeindeChange"
      />
    </div>

    <!-- No Kommune selected -->
    <div
      v-if="selectedGemeindeId === null"
      class="flex flex-col items-center justify-center gap-3 py-16 px-4 text-center rounded-xl border border-dashed border-gray-300 dark:border-gray-600"
    >
      <i class="pi pi-building text-4xl text-gray-300 dark:text-gray-600" />
      <div class="font-semibold">Keine Kommune ausgewählt</div>
      <p class="text-sm text-gray-500 dark:text-gray-400">
        Wähle eine Kommune aus, um deren veröffentlichte Magistratsvorlagen zu sehen.
      </p>
      <Select
        v-model="selectedGemeindeId"
        :options="gemeinden"
        optionLabel="name"
        optionValue="id"
        placeholder="Kommune auswählen"
        aria-label="Kommune auswählen"
        class="w-full max-w-xs mt-2"
        :loading="isLoadingGemeinden"
        filter
        filterPlaceholder="Suchen..."
        @change="onGemeindeChange"
      />
    </div>

    <template v-else>
      <!-- Toolbar -->
      <div class="flex flex-col md:flex-row md:items-center gap-3 mb-4">
        <IconField class="w-full md:max-w-md">
          <InputIcon class="pi pi-search" />
          <InputText
            v-model="searchQuery"
            placeholder="Nach Magistratsvorlage suchen"
            class="w-full"
            aria-label="Nach Magistratsvorlage suchen"
          />
        </IconField>
        <span
          v-if="!isLoadingVorlagen"
          class="text-sm text-gray-500 dark:text-gray-400 whitespace-nowrap"
          aria-live="polite"
        >
          {{ filteredVorlagen.length }}
          {{ filteredVorlagen.length === 1 ? 'Magistratsvorlage' : 'Magistratsvorlagen' }}
          <span v-if="filteredVorlagen.length !== magistratsvorlagen.length">
            von {{ magistratsvorlagen.length }}
          </span>
        </span>
        <div class="flex items-center gap-2 md:ml-auto">
          <Button
            v-if="hatAktiveFilter"
            v-tooltip.top="'Filter zurücksetzen'"
            icon="pi pi-filter-slash"
            aria-label="Filter zurücksetzen"
            @click="resetFilters"
            severity="secondary"
            variant="text"
          />
          <Button
            label="Filter"
            icon="pi pi-sliders-h"
            @click="drawerVisible = true"
            :badge="countFilter > 0 ? String(countFilter) : undefined"
            severity="secondary"
            outlined
          />
        </div>
      </div>

      <Drawer v-model:visible="drawerVisible" header="Filter" position="right">
        <div class="grid grid-cols-1 gap-4">
          <div v-if="vorgangOptions.length">
            <label class="mb-2 block font-bold">Verwaltungsvorgänge</label>
            <Listbox
              v-model="selectedVorgaenge"
              :options="vorgangOptions"
              class="w-full"
              multiple
            />
          </div>
          <div v-if="gebietOptions.length">
            <label class="mb-2 block font-bold">Gebiet</label>
            <Listbox
              v-model="selectedGebiete"
              :options="gebietOptions"
              optionLabel="name"
              optionValue="id"
              class="w-full"
              multiple
            />
          </div>
          <div v-if="tagOptions.length">
            <label class="mb-2 block font-bold">Tag</label>
            <Listbox
              v-model="selectedTags"
              :options="tagOptions"
              optionLabel="name"
              optionValue="id"
              class="w-full"
              multiple
            />
          </div>

          <DatePicker
            v-model="selectedDatum"
            placeholder="Datum auswählen"
            showIcon
            selectionMode="range"
            :manualInput="false"
            class="w-full"
          />
          <Card>
            <template #content>
              <div class="flex items-center justify-between">
                <label>Mobilitätscheck vorhanden</label>
                <ToggleSwitch v-model="filterMobilitaetscheckVorhanden" />
              </div>
            </template>
          </Card>

          <Button
            icon="pi pi-undo"
            label="Filter zurücksetzen"
            @click="resetFilters"
            severity="secondary"
            outlined
          />
        </div>
      </Drawer>

      <DataView
        :value="isLoadingVorlagen ? Array(5).fill({}) : filteredVorlagen"
        :paginator="!isLoadingVorlagen"
        :rows="20"
        :rowsPerPageOptions="[10, 20, 50]"
        class="vorlagen-liste"
      >
        <template #empty>
          <div
            class="flex flex-col items-center justify-center gap-3 py-16 text-center rounded-xl border border-dashed border-gray-300 dark:border-gray-600"
          >
            <i class="pi pi-inbox text-4xl text-gray-300 dark:text-gray-600" />
            <template v-if="magistratsvorlagen.length === 0">
              <div class="font-semibold">Keine veröffentlichten Magistratsvorlagen</div>
              <p class="text-sm text-gray-500 dark:text-gray-400">
                Für diese Kommune sind noch keine Magistratsvorlagen veröffentlicht.
              </p>
            </template>
            <template v-else>
              <div class="font-semibold">Keine Magistratsvorlagen gefunden</div>
              <p class="text-sm text-gray-500 dark:text-gray-400">
                Passe die Suche oder die Filter an.
              </p>
              <Button
                label="Filter zurücksetzen"
                icon="pi pi-filter-slash"
                size="small"
                severity="secondary"
                outlined
                @click="resetFilters"
              />
            </template>
          </div>
        </template>
        <template #list="slotProps">
          <ul
            class="overflow-hidden rounded-xl border border-gray-200 bg-white divide-y divide-gray-200 dark:bg-gray-800 dark:border-gray-700 dark:divide-gray-700"
          >
            <template v-if="isLoadingVorlagen">
              <li
                v-for="(_, i) in slotProps.items"
                :key="i"
                class="flex flex-col md:flex-row md:items-center gap-4 px-5 py-4"
              >
                <div class="flex-1 flex flex-col gap-2">
                  <Skeleton width="60%" height="1.25rem" />
                  <Skeleton width="12rem" height="0.875rem" />
                  <div class="flex gap-2">
                    <Skeleton width="5rem" height="1.5rem" borderRadius="1rem" />
                    <Skeleton width="4rem" height="1.5rem" borderRadius="1rem" />
                  </div>
                </div>
                <Skeleton width="9rem" height="2rem" borderRadius="1rem" />
              </li>
            </template>
            <template v-else>
              <li v-for="item in slotProps.items" :key="item.id">
                <router-link
                  :to="{
                    name: 'oeffentlich-magistratsvorlage-id',
                    params: { id: item.id },
                    query: { gemeinde: selectedGemeindeId }
                  }"
                  custom
                  v-slot="{ navigate, href }"
                >
                  <div
                    role="link"
                    tabindex="0"
                    :data-href="href"
                    class="vorlage-zeile group flex flex-col md:flex-row md:items-center gap-4 px-5 py-4 cursor-pointer transition-colors hover:bg-gray-50 dark:hover:bg-gray-700/50 focus-visible:outline-none focus-visible:bg-gray-50"
                    @click="navigate"
                    @keydown.enter.prevent="navigate"
                    @keydown.space.prevent="navigate"
                  >
                    <div class="flex-1 min-w-0">
                      <div
                        class="font-semibold text-base leading-snug text-gray-900 dark:text-gray-100 group-hover:text-[var(--p-primary-700)]"
                      >
                        {{ item.name }}
                      </div>
                      <div
                        class="mt-1 flex flex-wrap items-center gap-x-4 gap-y-1 text-sm text-gray-500 dark:text-gray-400"
                      >
                        <span
                          v-if="item.verwaltungsvorgangNr"
                          class="inline-flex items-center gap-1.5"
                        >
                          <i class="pi pi-hashtag text-xs" aria-hidden="true" />
                          <span class="sr-only">Nr.</span>{{ item.verwaltungsvorgangNr }}
                        </span>
                        <span
                          v-if="item.verwaltungsvorgangDatum"
                          class="inline-flex items-center gap-1.5"
                        >
                          <i class="pi pi-calendar text-xs" aria-hidden="true" />
                          <span class="sr-only">Datum</span>
                          {{ datumFormatieren(item.verwaltungsvorgangDatum) }}
                        </span>
                      </div>
                      <div
                        v-if="item.gemeindeGebiete?.length || item.tags?.length"
                        class="mt-2 flex flex-wrap items-center gap-1.5"
                      >
                        <Tag
                          v-for="gebiet in item.gemeindeGebiete"
                          :key="'g' + gebiet.id"
                          :value="gebiet.name"
                          icon="pi pi-map-marker"
                          severity="secondary"
                          rounded
                        />
                        <Tag
                          v-for="tag in item.tags"
                          :key="'t' + tag.id"
                          :value="'#' + tag.name"
                          severity="info"
                          rounded
                        />
                      </div>
                    </div>

                    <div class="flex flex-wrap items-center gap-2 md:justify-end">
                      <Tag
                        :icon="item.mobilitaetschecks?.length ? 'pi pi-check-circle' : 'pi pi-circle'"
                        value="Mobilitätscheck"
                        :severity="item.mobilitaetschecks?.length ? 'success' : 'secondary'"
                        rounded
                        class="status-tag"
                        :class="item.mobilitaetschecks?.length ? 'status-vorhanden' : 'status-fehlt'"
                        :aria-label="
                          'Mobilitätscheck ' +
                          (item.mobilitaetschecks?.length ? 'vorhanden' : 'nicht vorhanden')
                        "
                      />
                      <i
                        class="pi pi-chevron-right hidden md:block ml-2 text-gray-300 transition-transform group-hover:translate-x-0.5 group-hover:text-gray-500"
                        aria-hidden="true"
                      />
                    </div>
                  </div>
                </router-link>
              </li>
            </template>
          </ul>
        </template>
      </DataView>
    </template>
  </div>
</template>

<script setup>
import { ref, computed, watch, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { apiClient } from '@/services/axios'
import Button from 'openvue/button'
import Card from 'openvue/card'
import DataView from 'openvue/dataview'
import DatePicker from 'openvue/datepicker'
import Drawer from 'openvue/drawer'
import IconField from 'openvue/iconfield'
import InputIcon from 'openvue/inputicon'
import InputText from 'openvue/inputtext'
import Listbox from 'openvue/listbox'
import Select from 'openvue/select'
import Skeleton from 'openvue/skeleton'
import Tag from 'openvue/tag'
import ToggleSwitch from 'openvue/toggleswitch'

const route = useRoute()
const router = useRouter()

const gemeinden = ref([])
const selectedGemeindeId = ref(null)
const magistratsvorlagen = ref([])
const searchQuery = ref('')
const isLoadingGemeinden = ref(true)
const isLoadingVorlagen = ref(false)

// Filter
const drawerVisible = ref(false)
const selectedVorgaenge = ref([])
const selectedGebiete = ref([])
const selectedTags = ref([])
const selectedDatum = ref(null)
const filterMobilitaetscheckVorhanden = ref(false)

// Filter options are derived from the loaded Vorlagen (public endpoints only)
const uniqueById = (items) =>
  [...new Map(items.map((i) => [i.id, i])).values()].sort((a, b) =>
    a.name.localeCompare(b.name, 'de')
  )
const vorgangOptions = computed(() =>
  [...new Set(magistratsvorlagen.value.map((v) => v.verwaltungsvorgangNr).filter(Boolean))].sort()
)
const gebietOptions = computed(() =>
  uniqueById(magistratsvorlagen.value.flatMap((v) => v.gemeindeGebiete || []))
)
const tagOptions = computed(() => uniqueById(magistratsvorlagen.value.flatMap((v) => v.tags || [])))

const countFilter = computed(
  () =>
    [
      selectedVorgaenge.value.length > 0,
      selectedGebiete.value.length > 0,
      selectedTags.value.length > 0,
      selectedDatum.value?.length === 2 && !!selectedDatum.value[1],
      filterMobilitaetscheckVorhanden.value
    ].filter(Boolean).length
)

const hatAktiveFilter = computed(() => countFilter.value > 0 || !!searchQuery.value)

const resetFilters = () => {
  searchQuery.value = ''
  selectedVorgaenge.value = []
  selectedGebiete.value = []
  selectedTags.value = []
  selectedDatum.value = null
  filterMobilitaetscheckVorhanden.value = false
}

const filteredVorlagen = computed(() => {
  const q = searchQuery.value.trim().toLowerCase()
  return magistratsvorlagen.value.filter((v) => {
    if (
      q &&
      !v.name?.toLowerCase().includes(q) &&
      !v.verwaltungsvorgangNr?.toLowerCase().includes(q)
    )
      return false
    if (selectedVorgaenge.value.length && !selectedVorgaenge.value.includes(v.verwaltungsvorgangNr))
      return false
    if (
      selectedGebiete.value.length &&
      !v.gemeindeGebiete?.some((g) => selectedGebiete.value.includes(g.id))
    )
      return false
    if (selectedTags.value.length && !v.tags?.some((t) => selectedTags.value.includes(t.id)))
      return false
    if (selectedDatum.value?.length === 2 && selectedDatum.value[1]) {
      const [start, end] = selectedDatum.value
      const d = new Date(v.verwaltungsvorgangDatum)
      if (d < new Date(start) || d > new Date(end)) return false
    }
    if (filterMobilitaetscheckVorhanden.value && !v.mobilitaetschecks?.length) return false
    return true
  })
})

const fetchGemeinden = async () => {
  isLoadingGemeinden.value = true
  const res = await apiClient.get('/public/gemeinden')
  gemeinden.value = res.data
  isLoadingGemeinden.value = false
}

const fetchMagistratsvorlagen = async (gemeindeId) => {
  isLoadingVorlagen.value = true
  magistratsvorlagen.value = []
  const res = await apiClient.get('/public/magistratsvorlage', {
    params: { gemeinde_id: gemeindeId }
  })
  magistratsvorlagen.value = res.data
  isLoadingVorlagen.value = false
}

const onGemeindeChange = () => {
  resetFilters()
  router.replace({ query: { gemeinde: selectedGemeindeId.value } })
}

onMounted(async () => {
  await fetchGemeinden()
  const fromQuery = route.query.gemeinde ? Number(route.query.gemeinde) : null
  if (fromQuery) selectedGemeindeId.value = fromQuery
})

watch(selectedGemeindeId, (id) => {
  if (id) fetchMagistratsvorlagen(id)
  else magistratsvorlagen.value = []
})

const datumFormatieren = (datum) => {
  return new Date(datum).toLocaleDateString('de-DE', {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit'
  })
}
</script>

<style scoped>
.vorlagen-liste :deep(.p-dataview-content) {
  background: transparent;
}
.vorlagen-liste :deep(.p-paginator) {
  background: transparent;
  margin-top: 0.75rem;
}
.vorlage-zeile:focus-visible {
  box-shadow: inset 3px 0 0 var(--p-primary-color);
}
.status-tag {
  border: 1px solid transparent;
  padding: 0.375rem 0.75rem;
}
.status-vorhanden {
  background: var(--p-green-50, #f0fdf4);
  border-color: var(--p-green-200, #bbf7d0);
  color: var(--p-green-700, #15803d);
}
.status-fehlt {
  background: transparent;
  border: 1px dashed var(--p-gray-300, #d1d5db);
}
</style>
