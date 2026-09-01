<template>
  <div>
    <router-link
      :to="{ name: 'oeffentlich-magistratsvorlagen', query: { gemeinde: route.query.gemeinde } }"
    >
      <Button icon="pi pi-chevron-left" label="zur Übersicht" class="mb-5" severity="secondary" />
    </router-link>

    <BaseSpinner v-if="isLoading" class="m-10" />
    <template v-else-if="vorlage">
      <!-- Magistratsvorlage info card -->
      <BaseCard class="mb-6">
        <template #header>
          <span class="font-bold text-xl">{{ vorlage.name }}</span>
        </template>
        <div class="grid grid-cols-2 gap-x-8 gap-y-2 mt-2 text-sm max-w-xl">
          <span class="font-semibold">Vorgangsnummer</span>
          <span>{{ vorlage.verwaltungsvorgangNr }}</span>
          <span class="font-semibold">Datum</span>
          <span>{{ datumFormatieren(vorlage.verwaltungsvorgangDatum) }}</span>
          <template v-if="vorlage.beschreibung">
            <span class="font-semibold">Beschreibung</span>
            <span>{{ vorlage.beschreibung }}</span>
          </template>
          <template v-if="vorlage.gemeindeGebiete?.length > 0">
            <span class="font-semibold">Gebiete</span>
            <div class="flex flex-wrap gap-1">
              <Tag
                v-for="g in vorlage.gemeindeGebiete"
                :key="g.id"
                :value="g.name"
                severity="secondary"
              />
            </div>
          </template>
          <template v-if="vorlage.tags?.length > 0">
            <span class="font-semibold">Tags</span>
            <div class="flex flex-wrap gap-1">
              <Tag v-for="t in vorlage.tags" :key="t.id" :value="'#' + t.name" severity="info" />
            </div>
          </template>
        </div>
      </BaseCard>

      <!-- Tabs: Verwaltung / Politik -->
      <BaseSpinner v-if="isLoadingChecks" class="m-10" />
      <Tabs v-else value="verwaltung">
        <TabList>
          <Tab value="verwaltung">
            Verwaltung
            <Badge v-if="verwaltungChecks.length > 0" :value="verwaltungChecks.length" class="ml-2" />
          </Tab>
          <Tab value="politik">
            Politik
            <Badge v-if="politikChecks.length > 0" :value="politikChecks.length" class="ml-2" />
          </Tab>
        </TabList>
        <TabPanels>
          <TabPanel value="verwaltung">
            <p v-if="verwaltungChecks.length === 0" class="text-gray-500 py-4">
              Keine veröffentlichten Mobilitätschecks der Verwaltung vorhanden.
            </p>
            <div v-else class="flex flex-col gap-3 mt-3">
              <BaseCard v-for="check in verwaltungChecks" :key="check.id">
                <div class="col-span-10 grid grid-cols-1 gap-y-1">
                  <h3 class="font-bold text-lg">{{ check.name || 'Kein Name' }}</h3>
                  <div class="flex flex-wrap gap-x-6 gap-y-1 text-sm">
                    <div class="flex items-center gap-2">
                      <span class="font-semibold">Gruppe</span>
                      <span>{{ check.autor?.gruppe?.name || '–' }}</span>
                    </div>
                    <div class="flex items-center gap-2">
                      <span class="font-semibold">Erstellt am</span>
                      <span>{{ new Date(check.erstelltAm).toLocaleDateString('de-DE') }}</span>
                    </div>
                  </div>
                </div>
                <div class="col-span-2 flex items-center justify-end gap-2">
                  <Button icon="pi pi-eye" label="Anzeigen" size="small" @click="openModal(check)" />
                  <Button
                    icon="pi pi-download"
                    label="PDF-Export"
                    size="small"
                    :disabled="exportDisabled(check)"
                    @click="exportCheck(check.id)"
                  />
                </div>
              </BaseCard>
            </div>
          </TabPanel>

          <TabPanel value="politik">
            <p v-if="politikChecks.length === 0" class="text-gray-500 py-4">
              Keine veröffentlichten Mobilitätschecks der Politik vorhanden.
            </p>
            <div v-else class="flex flex-col gap-3 mt-3">
              <BaseCard v-for="check in politikChecks" :key="check.id">
                <div class="col-span-10 grid grid-cols-1 gap-y-1">
                  <h3 class="font-bold text-lg">{{ check.name || 'Kein Name' }}</h3>
                  <div class="flex flex-wrap gap-x-6 gap-y-1 text-sm">
                    <div class="flex items-center gap-2">
                      <span class="font-semibold">Erstellt von</span>
                      <span>
                        {{ check.autor?.vorname }} {{ check.autor?.nachname }}
                        <span v-if="check.autor?.gruppe?.name" class="text-gray-500 ml-1">
                          ({{ check.autor.gruppe.name }})
                        </span>
                      </span>
                    </div>
                    <div class="flex items-center gap-2">
                      <span class="font-semibold">Erstellt am</span>
                      <span>{{ new Date(check.erstelltAm).toLocaleDateString('de-DE') }}</span>
                    </div>
                  </div>
                </div>
                <div class="col-span-2 flex items-center justify-end gap-2">
                  <Button icon="pi pi-eye" label="Anzeigen" size="small" @click="openModal(check)" />
                  <Button
                    icon="pi pi-download"
                    label="PDF-Export"
                    size="small"
                    :disabled="exportDisabled(check)"
                    @click="exportCheck(check.id)"
                  />
                </div>
              </BaseCard>
            </div>
          </TabPanel>
        </TabPanels>
      </Tabs>
    </template>
    <p v-else class="text-gray-500">Magistratsvorlage nicht gefunden.</p>

    <!-- View modal -->
    <BaseModal v-model="modalVisible">
      <template #header>
        <h2>{{ activeCheck?.name || 'Kein Name' }} anzeigen</h2>
      </template>
      <MobilitaetscheckFormularEingabeZielOber
        v-if="activeCheck"
        :editMode="modalVisible"
        :readOnly="true"
        :item="activeCheck"
        @close-modal="modalVisible = false"
      />
    </BaseModal>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { apiClient } from '@/services/axios'
import { toastService } from '@/services/toast'
import BaseSpinner from '@/components/BaseSpinner.vue'
import MobilitaetscheckFormularEingabeZielOber from '@/components/MobilitaetscheckFormularEingabeZielOber.vue'
import Badge from 'primevue/badge'
import Button from 'primevue/button'
import Tab from 'primevue/tab'
import TabList from 'primevue/tablist'
import TabPanel from 'primevue/tabpanel'
import TabPanels from 'primevue/tabpanels'
import Tabs from 'primevue/tabs'
import Tag from 'primevue/tag'

const route = useRoute()

const vorlage = ref(null)
const mobilitaetschecks = ref([])
const isLoading = ref(true)
const isLoadingChecks = ref(true)
const modalVisible = ref(false)
const activeCheck = ref(null)

const verwaltungChecks = computed(() =>
  mobilitaetschecks.value.filter((c) => c.autor?.rolle?.name === 'Verwaltung')
)
const politikChecks = computed(() =>
  mobilitaetschecks.value.filter((c) => c.autor?.rolle?.name === 'Politik')
)

onMounted(async () => {
  const id = route.params.id
  try {
    const [mvRes, checksRes] = await Promise.all([
      apiClient.get(`/public/magistratsvorlage/${id}`),
      apiClient.get(`/public/mobilitaetscheck/magistratsvorlage/${id}`)
    ])
    vorlage.value = mvRes.data
    mobilitaetschecks.value = checksRes.data
  } catch {
    vorlage.value = null
  } finally {
    isLoading.value = false
    isLoadingChecks.value = false
  }
})

const datumFormatieren = (datum) => {
  if (!datum) return '–'
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
    toastService.add({ severity: 'success', detail: 'Mobilitätscheck erfolgreich exportiert' })
  } catch {
    toastService.add({ severity: 'error', detail: 'Fehler beim Exportieren des Mobilitätschecks' })
  }
}
</script>
