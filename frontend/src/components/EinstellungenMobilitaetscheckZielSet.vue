<template>
  <div>
    <!-- Dialog: Neue Leitziele erstellen -->
    <BaseModal v-model="isCreateModalOpen">
      <template #header>
        <h2>Neue Leitziele erstellen</h2>
      </template>
      <div class="flex flex-col gap-4">
        <div class="flex flex-col gap-1">
          <label for="createName" class="font-semibold">Name *</label>
          <InputText id="createName" v-model="createForm.name" class="w-full" />
        </div>
        <div class="flex flex-col gap-1">
          <label for="createBeschreibung" class="font-semibold">Beschreibung</label>
          <Textarea id="createBeschreibung" v-model="createForm.beschreibung" rows="3" class="w-full" />
        </div>
        <div class="flex items-center gap-2">
          <ToggleSwitch v-model="createForm.istOeffentlich" inputId="createOeffentlich" />
          <label for="createOeffentlich">Öffentlich sichtbar für andere Kommunen</label>
        </div>
      </div>
      <template #footer>
        <div class="flex gap-2 justify-end w-full">
          <Button label="Abbrechen" severity="secondary" size="small" @click="isCreateModalOpen = false" />
          <Button label="Erstellen" size="small" :disabled="!createForm.name" @click="onCreateSet" />
        </div>
      </template>
    </BaseModal>


    <!-- Dialog: Set bearbeiten -->
    <BaseModal v-model="isEditModalOpen">
      <template #header>
        <h2>Leitziele bearbeiten</h2>
      </template>
      <div class="flex flex-col gap-4">
        <div class="flex flex-col gap-1">
          <label for="editName" class="font-semibold">Name *</label>
          <InputText id="editName" v-model="editForm.name" class="w-full" />
        </div>
        <div class="flex flex-col gap-1">
          <label for="editBeschreibung" class="font-semibold">Beschreibung</label>
          <Textarea id="editBeschreibung" v-model="editForm.beschreibung" rows="3" class="w-full" />
        </div>
        <div class="flex items-center gap-2">
          <ToggleSwitch v-model="editForm.istOeffentlich" inputId="editOeffentlich" />
          <label for="editOeffentlich">Öffentlich sichtbar für andere Kommunen</label>
        </div>
      </div>
      <template #footer>
        <div class="flex gap-2 justify-end w-full">
          <Button label="Abbrechen" severity="secondary" size="small" @click="isEditModalOpen = false" />
          <Button label="Speichern" size="small" :disabled="!editForm.name" @click="onUpdateSet" />
        </div>
      </template>
    </BaseModal>

    <!-- Header -->
    <div class="flex gap-4 items-center mb-5">
      <BaseSubheading>Leitziele</BaseSubheading>
    </div>

    <BaseSpinner v-if="isLoading" class="m-10" />

    <div v-else>
      <BaseTabs :tabs="tabs" :disableUrlAltering="false">
        <!-- Tab: Meine Sets -->
        <template #meine-sets>
          <div class="mt-4">
            <div class="flex items-start gap-2 mb-4 p-3 bg-blue-50 border border-blue-200 rounded text-sm text-blue-800">
              <i class="pi pi-info-circle mt-0.5 shrink-0" />
              <span>
                Änderungen an den Leitzielen wirken sich auf bestehende Mobilitätschecks aus.
                Wird ein Ober- oder Unterziel gelöscht, entfällt es auch in allen bereits erstellten Mobilitätschecks.
                Für Tests empfiehlt es sich, die Leitziele zunächst zu <strong>duplizieren</strong> und die Änderungen an der Kopie vorzunehmen.
              </span>
            </div>
            <div class="flex gap-2 mb-4">
              <Button
                label="Neue Leitziele erstellen"
                icon="pi pi-plus"
                size="small"
                @click="openCreateModal"
              />
            </div>

            <div v-if="meineSets.length === 0" class="text-gray-500 m-5">
              Noch keine eigenen Leitziele vorhanden.
            </div>

            <div v-for="set in meineSets" :key="set.id" class="mb-3">
              <BaseCard :collapsible="true" :initiallyCollapsed="set.id !== neuesSetId && set.hatZiele">
                <template #header>
                  <div class="grid grid-cols-12 gap-2 items-center p-2">
                    <div class="col-span-9 flex items-center gap-2 flex-wrap">
                      <span class="font-bold">{{ set.name }}</span>
                      <span
                        v-if="set.istStandard"
                        class="text-xs bg-yellow-100 text-yellow-700 px-2 py-0.5 rounded-full"
                      >
                        Standard
                      </span>
                      <span
                        v-if="set.istOeffentlich"
                        class="text-xs bg-green-100 text-green-700 px-2 py-0.5 rounded-full"
                      >
                        öffentlich
                      </span>
                      <span v-else class="text-xs bg-gray-100 text-gray-500 px-2 py-0.5 rounded-full">
                        privat
                      </span>
                      <span v-if="set.beschreibung" class="text-sm text-gray-500 truncate max-w-sm">
                        {{ set.beschreibung }}
                      </span>
                    </div>
                    <div class="col-span-3 flex gap-1 justify-end">
                      <Button
                        v-if="!set.istStandard"
                        icon="pi pi-star"
                        size="small"
                        severity="secondary"
                        rounded
                        v-tooltip="'Als Standard setzen'"
                        @click.stop="onSetAlsStandard(set)"
                      />
                      <Button
                        v-else
                        icon="pi pi-star-fill"
                        size="small"
                        severity="warn"
                        rounded
                        v-tooltip="'Standard entfernen'"
                        @click.stop="onClearStandard"
                      />
                      <Button
                        icon="pi pi-copy"
                        size="small"
                        severity="secondary"
                        rounded
                        v-tooltip="'Duplizieren'"
                        @click.stop="onDuplizieren(set)"
                      />
                      <Button
                        icon="pi pi-pencil"
                        size="small"
                        severity="secondary"
                        rounded
                        v-tooltip="'Bearbeiten'"
                        @click.stop="openEditModal(set)"
                      />
                      <ButtonLoeschen noLabel @delete-confirmed="onDeleteSet(set.id)">
                        <p class="text-amber-700 text-sm mt-2">
                          Achtung: Mobilitätschecks, die auf diesen Leitzielen basieren, sind danach möglicherweise nicht mehr vollständig zugänglich.
                        </p>
                      </ButtonLoeschen>
                    </div>
                  </div>
                </template>

                <!-- Expandable: Ziele content (loaded lazily when card expands) -->
                <ZielSetInhalt :set="set" :editable="true" />
              </BaseCard>
            </div>
          </div>
        </template>

        <!-- Tab: Öffentliche Sets -->
        <template #oeffentliche-sets>
          <div class="mt-4">
            <div v-if="oeffentlicheSets.length === 0" class="text-gray-500 m-5">
              Keine Leitziele anderer Kommunen vorhanden.
            </div>

            <div v-for="set in oeffentlicheSets" :key="set.id" class="mb-3">
              <BaseCard :collapsible="true" :initiallyCollapsed="true">
                <template #header>
                  <div class="grid grid-cols-12 gap-2 items-center p-2">
                    <div class="col-span-9 flex items-center gap-2 flex-wrap">
                      <span class="font-bold">{{ set.gemeinde?.name }}</span>
                      <span class="text-sm text-gray-500">{{ set.name }}</span>
                      <span
                        v-if="set.istStandard"
                        class="text-xs bg-yellow-100 text-yellow-700 px-2 py-0.5 rounded-full"
                      >
                        Standard
                      </span>
                      <span v-if="set.beschreibung" class="text-sm text-gray-500 truncate max-w-sm">
                        {{ set.beschreibung }}
                      </span>
                    </div>
                    <div class="col-span-3 flex gap-1 justify-end">
                      <Button
                        v-if="!set.istStandard"
                        icon="pi pi-star"
                        size="small"
                        severity="secondary"
                        rounded
                        v-tooltip="'Als Standard setzen'"
                        @click.stop="onSetAlsStandard(set)"
                      />
                      <Button
                        v-else
                        icon="pi pi-star-fill"
                        size="small"
                        severity="warn"
                        rounded
                        v-tooltip="'Standard entfernen'"
                        @click.stop="onClearStandard"
                      />
                      <Button
                        label="Übernehmen"
                        icon="pi pi-download"
                        size="small"
                        severity="secondary"
                        @click.stop="onDuplizieren(set)"
                      />
                    </div>
                  </div>
                </template>

                <ZielSetInhalt :set="set" />
              </BaseCard>
            </div>
          </div>
        </template>
      </BaseTabs>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { fetchItems, deleteItem, updateItem } from '@/composables/crud'
import { apiClient } from '@/services/axios'
import { toastService } from '@/services/toast'
import { useAuthStore } from '@/stores/auth'
import { useRouter } from 'vue-router'
import Button from 'openvue/button'
import InputText from 'openvue/inputtext'
import Textarea from 'openvue/textarea'
import ToggleSwitch from 'openvue/toggleswitch'
import BaseModal from '@/components/BaseModal.vue'
import BaseCard from '@/components/BaseCard.vue'
import BaseSpinner from '@/components/BaseSpinner.vue'
import BaseSubheading from '@/components/BaseSubheading.vue'
import BaseTabs from '@/components/BaseTabs.vue'
import ButtonLoeschen from '@/components/ButtonLoeschen.vue'
import ZielSetInhalt from '@/components/EinstellungenMobilitaetscheckZielSetInhalt.vue'

const API_PATH = 'einstellungen/mobilitaetscheck/ziel-set'

const tabs = [
  { name: 'meine-sets', label: 'Meine Kommune' },
  { name: 'oeffentliche-sets', label: 'Weitere Leitziele' }
]

const authStore = useAuthStore()
const router = useRouter()
const isLoading = ref(false)
const alleSets = ref([])
const neuesSetId = ref(null)

const meineSets = computed(() =>
  alleSets.value.filter((s) => s.gemeindeId === authStore.gemeindeId)
)

const oeffentlicheSets = computed(() =>
  alleSets.value.filter(
    (s) => s.gemeindeId !== authStore.gemeindeId && s.istOeffentlich
  )
)

onMounted(async () => {
  await fetchSets()
})

const fetchSets = async () => {
  isLoading.value = true
  const data = await fetchItems(`/${API_PATH}`)
  alleSets.value = Array.isArray(data) ? data : []
  isLoading.value = false
}

// --- Create Set ---
const isCreateModalOpen = ref(false)
const createForm = ref({ name: '', beschreibung: '', istOeffentlich: false })

const openCreateModal = () => {
  createForm.value = { name: '', beschreibung: '', istOeffentlich: false }
  isCreateModalOpen.value = true
}

const onCreateSet = async () => {
  try {
    const response = await apiClient.post(`/${API_PATH}`, {
      name: createForm.value.name,
      beschreibung: createForm.value.beschreibung || null,
      istOeffentlich: createForm.value.istOeffentlich,
      zieleOber: []
    })
    alleSets.value.unshift(response.data)
    neuesSetId.value = response.data.id
    toastService.add({ severity: 'success', detail: 'Leitziele erfolgreich erstellt' })
    isCreateModalOpen.value = false
  } catch (e) {
    toastService.add({ severity: 'error', detail: 'Fehler beim Erstellen der Leitziele' })
  }
}


// --- Edit Set ---
const isEditModalOpen = ref(false)
const editForm = ref({ id: null, name: '', beschreibung: '', istOeffentlich: false })

const openEditModal = (set) => {
  editForm.value = {
    id: set.id,
    name: set.name,
    beschreibung: set.beschreibung || '',
    istOeffentlich: set.istOeffentlich
  }
  isEditModalOpen.value = true
}

const onUpdateSet = async () => {
  const response = await updateItem({
    model: API_PATH,
    modelId: editForm.value.id,
    values: {
      name: editForm.value.name,
      beschreibung: editForm.value.beschreibung || null,
      istOeffentlich: editForm.value.istOeffentlich
    },
    detail: {
      success: 'Leitziele erfolgreich aktualisiert',
      error: 'Fehler beim Aktualisieren der Leitziele'
    }
  })
  if (response) {
    const ix = alleSets.value.findIndex((s) => s.id === response.id)
    if (ix !== -1) {
      alleSets.value.splice(ix, 1, { ...alleSets.value[ix], ...response })
    }
    isEditModalOpen.value = false
  }
}

// --- Delete Set ---
const onDeleteSet = async (id) => {
  await deleteItem({
    model: API_PATH,
    modelId: id,
    detail: {
      success: 'Leitziele erfolgreich gelöscht',
      error: 'Fehler beim Löschen der Leitziele'
    }
  })
  const ix = alleSets.value.findIndex((s) => s.id === id)
  if (ix !== -1) {
    alleSets.value.splice(ix, 1)
  }
}

// --- Duplizieren ---
const onDuplizieren = async (set) => {
  try {
    const response = await apiClient.post(`/${API_PATH}/${set.id}/duplizieren`)
    alleSets.value.unshift(response.data)
    neuesSetId.value = response.data.id
    toastService.add({ severity: 'success', detail: 'Leitziele erfolgreich übernommen' })
    router.push({ query: { tab: 'meine-sets' } })
  } catch {
    toastService.add({ severity: 'error', detail: 'Fehler beim Übernehmen der Leitziele' })
  }
}

// --- Standard setzen / entfernen ---
const onSetAlsStandard = async (set) => {
  try {
    await apiClient.post(`/${API_PATH}/${set.id}/als-standard-setzen`)
    await fetchSets()
    toastService.add({ severity: 'success', detail: 'Standard-Leitziele gesetzt' })
  } catch (e) {
    toastService.add({ severity: 'error', detail: 'Fehler beim Setzen des Standards' })
  }
}

const onClearStandard = async () => {
  try {
    await apiClient.delete(`/${API_PATH}/standard`)
    await fetchSets()
    toastService.add({ severity: 'success', detail: 'Standard-Leitziele entfernt' })
  } catch (e) {
    toastService.add({ severity: 'error', detail: 'Fehler beim Entfernen des Standards' })
  }
}

</script>

<style scoped></style>
