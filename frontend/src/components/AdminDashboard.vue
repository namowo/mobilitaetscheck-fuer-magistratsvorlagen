<template>
  <div>
    <div class="flex items-center justify-between mb-4">
      <h5 class="text-lg font-semibold">Dashboard</h5>
      <SelectButton
        v-model="selectedRange"
        :options="rangeOptions"
        optionLabel="label"
        optionValue="value"
        :allowEmpty="false"
        size="small"
      />
    </div>

    <BaseSpinner v-if="isLoading" />
    <div v-else-if="stats">
      <div class="grid grid-cols-2 md:grid-cols-3 gap-3 mb-4">
        <StatTile label="Benutzer" :value="stats.anzahlUser" icon="pi pi-users" />
        <StatTile label="Kommunen" :value="stats.anzahlGemeinden" icon="pi pi-building" />
        <StatTile
          label="Magistratsvorlagen"
          :value="stats.anzahlMagistratsvorlagen"
          icon="pi pi-file"
        />
        <StatTile
          label="davon veröffentlicht"
          :value="stats.magistratsvorlagenVeroeffentlicht"
          icon="pi pi-check-circle"
        />
        <StatTile
          label="Mobilitätschecks"
          :value="stats.anzahlMobilitaetschecks"
          icon="pi pi-map"
        />
        <StatTile
          label="Klimarelevanzprüfungen"
          :value="stats.anzahlKlimarelevanzpruefungen"
          icon="pi pi-sun"
        />
      </div>

      <div class="grid grid-cols-1 lg:grid-cols-2 gap-3">
        <BaseCard>
          <template #header>
            <h5 class="text-lg font-semibold mb-3 min-h-[2.75rem] flex items-center">Benutzer pro Monat</h5>
          </template>
          <MonthlyBarChart :data="stats.neueUserProMonat" />
        </BaseCard>

        <BaseCard>
          <template #header>
            <h5 class="text-lg font-semibold mb-3 min-h-[2.75rem] flex items-center">Magistratsvorlagen pro Monat</h5>
          </template>
          <MonthlyBarChart :data="stats.neueMagistratsvorlagenProMonat" />
        </BaseCard>

        <BaseCard>
          <template #header>
            <h5 class="text-lg font-semibold mb-3 min-h-[2.75rem] flex items-center">Mobilitätscheck pro Monat</h5>
          </template>
          <MonthlyBarChart :data="stats.neueMobilitaetschecksProMonat" />
        </BaseCard>

        <BaseCard>
          <template #header>
            <h5 class="text-lg font-semibold mb-3 min-h-[2.75rem] flex items-center">Klimarelevanzprüfung pro Monat</h5>
          </template>
          <MonthlyBarChart :data="stats.neueKlimarelevanzpruefungenProMonat" />
        </BaseCard>

        <BaseCard>
          <template #header>
            <h5 class="text-lg font-semibold mb-3 min-h-[2.75rem] flex items-center">Magistratsvorlagen pro Kommune</h5>
          </template>
          <GemeindeBarChart :data="stats.magistratsvorlagenProGemeinde" />
        </BaseCard>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue'
import SelectButton from 'openvue/selectbutton'
import { apiClient } from '@/services/axios'
import StatTile from '@/components/dashboard/StatTile.vue'
import MonthlyBarChart from '@/components/dashboard/MonthlyBarChart.vue'
import GemeindeBarChart from '@/components/dashboard/GemeindeBarChart.vue'

const stats = ref(null)
const isLoading = ref(false)

const rangeOptions = [
  { label: '3 Monate', value: 3 },
  { label: '6 Monate', value: 6 },
  { label: '12 Monate', value: 12 },
  { label: 'Gesamt', value: null }
]
const selectedRange = ref(12)

const vonFuerRange = (monate) => {
  if (!monate) return null
  const d = new Date()
  d.setMonth(d.getMonth() - monate + 1)
  d.setDate(1)
  return d.toISOString().slice(0, 10)
}

const loadStats = async () => {
  isLoading.value = true
  try {
    const von = vonFuerRange(selectedRange.value)
    const res = await apiClient.get('/admin/dashboard/stats', {
      params: von ? { von } : {}
    })
    stats.value = res.data
  } catch {
    /* */
  } finally {
    isLoading.value = false
  }
}

onMounted(loadStats)
watch(selectedRange, loadStats)
</script>
