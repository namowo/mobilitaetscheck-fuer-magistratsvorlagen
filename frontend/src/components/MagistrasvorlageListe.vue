<template>
  <div>
    <Drawer v-model:visible="drawerVisible" header="Filter" position="right">
      <div class="grid grid-cols-1 gap-4">
        <div>
          <label class="mb-2 block font-bold">Verwaltungsvorgänge</label>
          <Listbox
            v-model="selectedVorgaenge"
            :options="vorgangOptions"
            class="w-full"
            multiple
            showClear
          />
        </div>
        <div>
          <label class="mb-2 block font-bold">Gebiet</label>
          <Listbox
            v-model="selectedGebiete"
            :options="gebietOptions"
            optionLabel="name"
            optionValue="id"
            class="w-full"
            multiple
            showClear
          />
        </div>
        <div>
          <label class="mb-2 block font-bold">Tag</label>
          <Listbox
            v-model="selectedTags"
            :options="tagOptions"
            optionLabel="name"
            optionValue="id"
            class="w-full"
            multiple
            showClear
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
            <div class="grid grid-cols-1 gap-4">
              <div class="flex items-center justify-between">
                <label>Mobilitätscheck vorhanden</label>
                <ToggleSwitch v-model="filterMobilitaetscheckVorhanden" />
              </div>
              <div v-if="authStore.klimacheckAktiv" class="flex items-center justify-between">
                <label>Klimacheck vorhanden</label>
                <ToggleSwitch v-model="filterKlimarelevanzpruefungVorhanden" />
              </div>
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

    <!-- Toolbar -->
    <div class="flex flex-col md:flex-row md:items-center gap-3 mb-4">
      <IconField class="w-full md:max-w-md" data-tour="vorlagen-suche">
        <InputIcon class="pi pi-search" />
        <InputText
          v-model="searchQuery"
          placeholder="Nach Magistratsvorlage suchen"
          class="w-full"
          aria-label="Nach Magistratsvorlage suchen"
        />
      </IconField>
      <p
        v-if="!isLoading"
        class="text-sm text-gray-500 dark:text-gray-400 whitespace-nowrap"
        aria-live="polite"
      >
        {{ filteredMagistratsvorlagen.length }}
        {{ filteredMagistratsvorlagen.length === 1 ? 'Magistratsvorlage' : 'Magistratsvorlagen' }}
        <span v-if="filteredMagistratsvorlagen.length !== magistratsvorlageListe.length">
          von {{ magistratsvorlageListe.length }}
        </span>
      </p>
      <div class="flex items-center gap-2 md:ml-auto">
        <SelectButton
          v-model="filterVonMirErstellt"
          :options="[
            { label: 'Alle', value: false, icon: 'pi pi-users' },
            { label: 'Von mir', value: true, icon: 'pi pi-user' }
          ]"
          optionLabel="label"
          optionValue="value"
          :allowEmpty="false"
        >
          <template #option="slotProps">
            <i :class="slotProps.option.icon"></i>
            <span class="ml-2">{{ slotProps.option.label }}</span>
          </template>
        </SelectButton>
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
          :badge="countFilter !== '0' ? countFilter : undefined"
          severity="secondary"
          outlined
        />
      </div>
    </div>

    <DataView
      :value="isLoading ? Array(5).fill({}) : filteredMagistratsvorlagen"
      :paginator="!isLoading"
      :rows="20"
      :rowsPerPageOptions="[10, 20, 50]"
      class="vorlagen-liste"
    >
      <template #empty>
        <div
          class="flex flex-col items-center justify-center gap-3 py-16 text-center rounded-xl border border-dashed border-gray-300 dark:border-gray-600"
        >
          <i class="pi pi-inbox text-4xl text-gray-300 dark:text-gray-600" />
          <div class="font-semibold">Keine Magistratsvorlagen gefunden</div>
          <p class="text-sm text-gray-500 dark:text-gray-400">
            Passe die Suche oder die Filter an.
          </p>
          <Button
            v-if="hatAktiveFilter"
            label="Filter zurücksetzen"
            icon="pi pi-filter-slash"
            size="small"
            severity="secondary"
            outlined
            @click="resetFilters"
          />
        </div>
      </template>
      <template #list="slotProps">
        <ul
          class="overflow-hidden rounded-xl border border-gray-200 bg-white divide-y divide-gray-200 dark:bg-gray-800 dark:border-gray-700 dark:divide-gray-700"
        >
          <template v-if="isLoading === true">
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
              <div class="flex gap-2">
                <Skeleton width="9rem" height="2rem" borderRadius="1rem" />
                <Skeleton width="7rem" height="2rem" borderRadius="1rem" />
              </div>
            </li>
          </template>
          <template v-else>
            <li v-for="item in slotProps.items" :key="item.id">
              <router-link
                :to="{ name: 'magistratsvorlage-id-daten', params: { id: item.id } }"
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
                      <span v-if="item.verwaltungsvorgangNr" class="inline-flex items-center gap-1.5">
                        <i class="pi pi-hashtag text-xs" aria-hidden="true" />
                        <span class="sr-only">Nr.</span>{{ item.verwaltungsvorgangNr }}
                      </span>
                      <span v-if="item.verwaltungsvorgangDatum" class="inline-flex items-center gap-1.5">
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

                  <div class="flex flex-wrap items-center gap-2 md:justify-end" @click.stop @keydown.stop>
                    <router-link
                      :to="{ name: 'magistratsvorlage-id-mobilitaetscheck', params: { id: item.id } }"
                      tabindex="-1"
                    >
                      <Button
                        :icon="item.mobilitaetschecks?.length ? 'pi pi-check-circle' : 'pi pi-circle'"
                        label="Mobilitätscheck"
                        :severity="item.mobilitaetschecks?.length ? 'success' : 'secondary'"
                        :variant="item.mobilitaetschecks?.length ? undefined : 'outlined'"
                        size="small"
                        rounded
                        :aria-label="
                          'Mobilitätscheck ' +
                          (item.mobilitaetschecks?.length ? 'vorhanden' : 'nicht vorhanden')
                        "
                        :class="item.mobilitaetschecks?.length ? 'status-vorhanden' : 'status-fehlt'"
                      />
                    </router-link>
                    <router-link
                      v-if="!isPolitik && authStore.klimacheckAktiv"
                      :to="{ name: 'magistratsvorlage-id-klimarelevanzpruefung', params: { id: item.id } }"
                      tabindex="-1"
                    >
                      <Button
                        :icon="item.klimarelevanzpruefungen?.length ? 'pi pi-check-circle' : 'pi pi-circle'"
                        label="Klimacheck"
                        :severity="item.klimarelevanzpruefungen?.length ? 'success' : 'secondary'"
                        :variant="item.klimarelevanzpruefungen?.length ? undefined : 'outlined'"
                        size="small"
                        rounded
                        :aria-label="
                          'Klimacheck ' +
                          (item.klimarelevanzpruefungen?.length ? 'vorhanden' : 'nicht vorhanden')
                        "
                        :class="item.klimarelevanzpruefungen?.length ? 'status-vorhanden' : 'status-fehlt'"
                      />
                    </router-link>
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
  </div>
</template>

<script setup>
import { computed, ref, onMounted } from 'vue'
import { fetchItems } from '@/composables/crud'
import { useAuthStore } from '@/stores/auth'
import Button from 'openvue/button'
import Card from 'openvue/card'
import DataView from 'openvue/dataview'
import DatePicker from 'openvue/datepicker'
import Drawer from 'openvue/drawer'
import IconField from 'openvue/iconfield'
import InputIcon from 'openvue/inputicon'
import InputText from 'openvue/inputtext'
import Tag from 'openvue/tag'
import SelectButton from 'openvue/selectbutton'
import Skeleton from 'openvue/skeleton'
import ToggleSwitch from 'openvue/toggleswitch'
import Listbox from 'openvue/listbox'

const authStore = useAuthStore()
const isPolitik = computed(() => authStore.effectiveRolleId === 2)

const magistratsvorlageListe = ref([])
const searchQuery = ref('')
const selectedGebiete = ref([])
const selectedTags = ref([])
const selectedDatum = ref()
const selectedVorgaenge = ref([])
const gebietOptions = ref([])
const tagOptions = ref([])
const vorgangOptions = ref([])
const isLoading = ref(true)
const drawerVisible = ref(false)
const filterMobilitaetscheckVorhanden = ref(false)
const filterKlimacheckVorhanden = ref(false)
const filterKlimarelevanzpruefungVorhanden = ref(false)
const filterVonMirErstellt = ref(false)

onMounted(async () => {
  isLoading.value = true
  await fetchData()
  isLoading.value = false
})

const fetchData = async () => {
  magistratsvorlageListe.value = await fetchItems('/magistratsvorlage')
  gebietOptions.value = await fetchItems('/einstellungen/gebiet')
  tagOptions.value = await fetchItems('/einstellungen/tag')
  vorgangOptions.value = await fetchItems('/magistratsvorlage/vorgaenge')
}

const countFilter = computed(() => {
  let count = 0
  if (selectedVorgaenge.value.length > 0) count++
  if (selectedGebiete.value.length > 0) count++
  if (selectedTags.value.length > 0) count++
  if (selectedDatum.value && selectedDatum.value.length === 2) count++
  if (filterMobilitaetscheckVorhanden.value) count++
  if (filterKlimacheckVorhanden.value) count++
  if (filterKlimarelevanzpruefungVorhanden.value) count++
  if (filterVonMirErstellt.value) count++
  return String(count)
})

const hatAktiveFilter = computed(() => countFilter.value !== '0' || !!searchQuery.value)

const resetFilters = () => {
  selectedVorgaenge.value = []
  selectedGebiete.value = []
  selectedTags.value = []
  selectedDatum.value = null
  searchQuery.value = ''
  filterMobilitaetscheckVorhanden.value = false
  filterKlimacheckVorhanden.value = false
  filterKlimarelevanzpruefungVorhanden.value = false
  filterVonMirErstellt.value = false
}

const datumFormatieren = (datum) => {
  return new Date(datum).toLocaleDateString('de-DE', {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit'
  })
}

const filteredMagistratsvorlagen = computed(() => {
  const query = searchQuery.value?.toLowerCase().trim() || ''

  const extractVal = (s) => {
    if (s === null || s === undefined) return String(s)
    if (typeof s === 'object') return String(s.id ?? s.value ?? s)
    return String(s)
  }

  const selectedVorgangValues = (selectedVorgaenge.value || []).map(extractVal)
  const selectedGebieteValues = (selectedGebiete.value || []).map(extractVal)
  const selectedTagValues = (selectedTags.value || []).map(extractVal)

  return magistratsvorlageListe.value.filter((item) => {
    const matchName = !query || item.name?.toLowerCase().includes(query)

    const matchVorgang = (() => {
      if (!selectedVorgangValues || selectedVorgangValues.length === 0) return true
      return selectedVorgangValues.includes(String(item.verwaltungsvorgangNr))
    })()

    const matchGebiet =
      !selectedGebiete.value ||
      selectedGebiete.value.length === 0 ||
      item.gemeindeGebiete?.some((g) => selectedGebieteValues.includes(String(g.id)))

    const matchTag =
      !selectedTags.value ||
      selectedTags.value.length === 0 ||
      item.tags?.some((t) => selectedTagValues.includes(String(t.id)))

    const matchDatum = (() => {
      if (!selectedDatum.value || selectedDatum.value.length < 2) return true
      const [start, end] = selectedDatum.value
      const itemDate = new Date(item.verwaltungsvorgangDatum)
      return itemDate >= new Date(start) && itemDate <= new Date(end)
    })()

    const matchMobilitaetscheck =
      !filterMobilitaetscheckVorhanden.value ||
      (item.mobilitaetschecks && item.mobilitaetschecks.length > 0)

    const matchKlimacheck =
      !filterKlimacheckVorhanden.value || (item.klimachecks && item.klimachecks.length > 0)

    const matchKlimarelevanzpruefung =
      !filterKlimarelevanzpruefungVorhanden.value ||
      (item.klimarelevanzpruefung && item.klimarelevanzpruefung.length > 0) ||
      (item.klimarelevanzpruefungen && item.klimarelevanzpruefungen.length > 0)

    const matchVonMir = (() => {
      if (!filterVonMirErstellt.value) return true
      return localStorage.getItem('userId').includes(String(item.erstelltVon))
    })()

    return (
      matchName &&
      matchGebiet &&
      matchTag &&
      matchVorgang &&
      matchDatum &&
      matchMobilitaetscheck &&
      matchKlimacheck &&
      matchKlimarelevanzpruefung &&
      matchVonMir
    )
  })
})
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
.status-vorhanden {
  background: var(--p-green-50, #f0fdf4);
  border-color: var(--p-green-200, #bbf7d0);
  color: var(--p-green-700, #15803d);
}
.status-vorhanden:hover {
  background: var(--p-green-100, #dcfce7) !important;
  border-color: var(--p-green-300, #86efac) !important;
  color: var(--p-green-800, #166534) !important;
}
.status-fehlt {
  border-style: dashed;
}
</style>
