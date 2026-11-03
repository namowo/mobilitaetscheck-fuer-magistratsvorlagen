<template>
  <div>
    <BaseCard>
      <div class="flex items-center justify-between mb-4">
        <h5 class="text-lg font-semibold">Kommunen</h5>
        <Button icon="pi pi-plus" label="Neue Kommune" @click="openCreate" />
      </div>

      <InputText v-model="searchQuery" placeholder="Kommune suchen…" class="w-full mb-4" />

      <BaseSpinner v-if="isLoading" />
      <DataTable v-else :value="filteredGemeinden" class="w-full">
        <template #empty>
          <span class="text-gray-400 text-sm">Keine Kommune gefunden.</span>
        </template>
        <Column field="name" header="Name" />
        <Column field="verwaltungEmailDomains" header="E-Mail-Domains">
          <template #body="{ data }">
            <div v-if="data.verwaltungEmailDomains?.length" class="flex flex-wrap gap-1">
              <Tag
                v-for="domain in data.verwaltungEmailDomains"
                :key="domain"
                :value="'@' + domain"
                severity="secondary"
              />
            </div>
            <span v-else class="text-gray-400 text-sm">–</span>
          </template>
        </Column>
        <Column header="" style="width: 100px">
          <template #body="{ data }">
            <div class="flex gap-1">
              <Button icon="pi pi-pencil" text @click="openEdit(data)" />
              <Button
                icon="pi pi-trash"
                severity="danger"
                text
                @click="deleteGemeinde(data.id)"
              />
            </div>
          </template>
        </Column>
      </DataTable>
    </BaseCard>

    <!-- Create Dialog -->
    <Dialog
      v-model:visible="createVisible"
      header="Neue Kommune anlegen"
      :modal="true"
      class="w-full max-w-sm"
    >
      <form @submit.prevent="submitCreate" class="mt-2 flex flex-col gap-4">
        <div class="field">
          <FloatLabel variant="on">
            <InputText
              id="newName"
              v-model="createName"
              class="w-full"
              :invalid="!!createErrors.name"
            />
            <label for="newName">Name</label>
          </FloatLabel>
          <small v-if="createErrors.name" class="text-red-600 text-sm block mt-1">{{
            createErrors.name
          }}</small>
        </div>
        <div class="field">
          <label for="newDomains" class="block text-sm text-gray-500 mb-1">E-Mail-Domains</label>
          <InputChips
            inputId="newDomains"
            v-model="createDomains"
            :allowDuplicate="false"
            separator=","
            addOnBlur
            :placeholder="createDomains?.length ? '' : 'beispielstadt.de'"
            class="w-full"
            :invalid="!!createErrors.verwaltungEmailDomains"
          />
          <small class="text-gray-400 text-xs block mt-1"
            >Mehrere Domains mit Enter oder Komma trennen.</small
          >
          <small
            v-if="createErrors.verwaltungEmailDomains"
            class="text-red-600 text-sm block mt-1"
            >{{ createErrors.verwaltungEmailDomains }}</small
          >
        </div>
        <div class="inline-field">
          <label for="createKlimacheck">Klimacheck aktivieren</label>
          <ToggleSwitch inputId="createKlimacheck" v-model="createKlimacheck" />
        </div>
      </form>
      <template #footer>
        <Button label="Abbrechen" text @click="createVisible = false" />
        <Button label="Anlegen" @click="submitCreate" :loading="isCreating" />
      </template>
    </Dialog>

    <!-- Edit Dialog -->
    <Dialog
      v-model:visible="editVisible"
      header="Kommune bearbeiten"
      :modal="true"
      class="w-full max-w-sm"
    >
      <form @submit.prevent="submitEdit" class="mt-2 flex flex-col gap-4">
        <div class="field">
          <FloatLabel variant="on">
            <InputText
              id="editName"
              v-model="editName"
              class="w-full"
              :invalid="!!editErrors.name"
            />
            <label for="editName">Name</label>
          </FloatLabel>
          <small v-if="editErrors.name" class="text-red-600 text-sm block mt-1">{{
            editErrors.name
          }}</small>
        </div>
        <div class="field">
          <label for="editDomains" class="block text-sm text-gray-500 mb-1">E-Mail-Domains</label>
          <InputChips
            inputId="editDomains"
            v-model="editDomains"
            :allowDuplicate="false"
            separator=","
            addOnBlur
            :placeholder="editDomains?.length ? '' : 'beispielstadt.de'"
            class="w-full"
            :invalid="!!editErrors.verwaltungEmailDomains"
          />
          <small class="text-gray-400 text-xs block mt-1"
            >Mehrere Domains mit Enter oder Komma trennen.</small
          >
          <small
            v-if="editErrors.verwaltungEmailDomains"
            class="text-red-600 text-sm block mt-1"
            >{{ editErrors.verwaltungEmailDomains }}</small
          >
        </div>
        <div class="inline-field">
          <label for="editKlimacheck">Klimacheck aktivieren</label>
          <ToggleSwitch inputId="editKlimacheck" v-model="editKlimacheck" />
        </div>
      </form>
      <template #footer>
        <Button label="Abbrechen" text @click="editVisible = false" />
        <Button label="Speichern" @click="submitEdit" :loading="isSaving" />
      </template>
    </Dialog>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { onKeyStroke } from '@vueuse/core'
import { useForm } from 'vee-validate'
import * as yup from 'yup'
import Button from 'openvue/button'
import InputText from 'openvue/inputtext'
import FloatLabel from 'openvue/floatlabel'
import InputChips from 'openvue/inputchips'
import Tag from 'openvue/tag'
import DataTable from 'openvue/datatable'
import Column from 'openvue/column'
import Dialog from 'openvue/dialog'
import ToggleSwitch from 'openvue/toggleswitch'
import { apiClient } from '@/services/axios'
import { useToast } from 'openvue/usetoast'

const gemeindeSchema = yup.object({
  name: yup.string().required('Name ist erforderlich.').label('Name'),
  verwaltungEmailDomains: yup
    .array()
    .of(
      yup
        .string()
        .trim()
        .matches(/^@?[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/, 'Ungültige Domain (z.B. beispielstadt.de).')
    )
    .default([])
    .label('E-Mail-Domains'),
  klimacheckAktiv: yup.boolean().default(false)
})

const gemeinden = ref([])
const isLoading = ref(false)
const searchQuery = ref('')

// --- Create form ---
const createVisible = ref(false)
const isCreating = ref(false)

const {
  defineField: defineCreateField,
  handleSubmit: handleCreate,
  errors: createErrors,
  resetForm: resetCreate
} = useForm({ validationSchema: gemeindeSchema })

const [createName] = defineCreateField('name')
const [createDomains] = defineCreateField('verwaltungEmailDomains')
const [createKlimacheck] = defineCreateField('klimacheckAktiv')

const openCreate = () => {
  resetCreate({ values: { name: '', verwaltungEmailDomains: [], klimacheckAktiv: false } })
  createVisible.value = true
}

// --- Edit form ---
const editVisible = ref(false)
const editId = ref(null)
const isSaving = ref(false)

const {
  defineField: defineEditField,
  handleSubmit: handleEdit,
  errors: editErrors,
  setValues: setEditValues
} = useForm({ validationSchema: gemeindeSchema })

const [editName] = defineEditField('name')
const [editDomains] = defineEditField('verwaltungEmailDomains')
const [editKlimacheck] = defineEditField('klimacheckAktiv')

// ---

const toast = useToast()

onKeyStroke('Enter', (e) => {
  if (createVisible.value) {
    e.preventDefault()
    submitCreate()
  }
  if (editVisible.value) {
    e.preventDefault()
    submitEdit()
  }
})

onKeyStroke('Escape', () => {
  if (createVisible.value) createVisible.value = false
  if (editVisible.value) editVisible.value = false
})

const SYSTEM_GEMEINDE_NAME = 'Systemadministration'

const filteredGemeinden = computed(() => {
  const visible = gemeinden.value.filter((g) => g.name !== SYSTEM_GEMEINDE_NAME)
  if (!searchQuery.value.trim()) return visible
  const q = searchQuery.value.toLowerCase()
  return visible.filter((g) => g.name.toLowerCase().includes(q))
})

const fetchGemeinden = async () => {
  isLoading.value = true
  try {
    const res = await apiClient.get('/admin/gemeinde')
    gemeinden.value = res.data
  } catch {
    gemeinden.value = []
  } finally {
    isLoading.value = false
  }
}

onMounted(fetchGemeinden)

const submitCreate = handleCreate(async (values) => {
  isCreating.value = true
  try {
    await apiClient.post('/admin/gemeinde', {
      name: values.name,
      verwaltung_email_domains: (values.verwaltungEmailDomains || []).map((d) => d.replace(/^@/, '')),
      klimacheck_aktiv: !!values.klimacheckAktiv
    })
    toast.add({ severity: 'success', summary: 'Kommune angelegt', life: 3000 })
    createVisible.value = false
    await fetchGemeinden()
  } catch {
    toast.add({
      severity: 'error',
      summary: 'Fehler',
      detail: 'Kommune konnte nicht angelegt werden.',
      life: 3000
    })
  } finally {
    isCreating.value = false
  }
})

const openEdit = (gemeinde) => {
  editId.value = gemeinde.id
  setEditValues({
    name: gemeinde.name,
    verwaltungEmailDomains: [...(gemeinde.verwaltungEmailDomains || [])],
    klimacheckAktiv: !!gemeinde.klimacheckAktiv
  })
  editVisible.value = true
}

const submitEdit = handleEdit(async (values) => {
  isSaving.value = true
  try {
    const res = await apiClient.patch(`/admin/gemeinde/${editId.value}`, {
      name: values.name,
      verwaltung_email_domains: (values.verwaltungEmailDomains || []).map((d) => d.replace(/^@/, '')),
      klimacheck_aktiv: !!values.klimacheckAktiv
    })
    const idx = gemeinden.value.findIndex((g) => g.id === editId.value)
    if (idx !== -1) gemeinden.value[idx] = res.data
    editVisible.value = false
    toast.add({ severity: 'success', summary: 'Gespeichert', life: 3000 })
  } catch {
    toast.add({
      severity: 'error',
      summary: 'Fehler',
      detail: 'Änderung konnte nicht gespeichert werden.',
      life: 3000
    })
  } finally {
    isSaving.value = false
  }
})

const deleteGemeinde = async (id) => {
  try {
    await apiClient.delete(`/admin/gemeinde/${id}`)
    gemeinden.value = gemeinden.value.filter((g) => g.id !== id)
    toast.add({ severity: 'success', summary: 'Kommune gelöscht', life: 3000 })
  } catch {
    toast.add({
      severity: 'error',
      summary: 'Fehler',
      detail: 'Kommune konnte nicht gelöscht werden.',
      life: 3000
    })
  }
}
</script>

<style scoped>
.inline-field {
  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: space-between;
  gap: 1rem;
}
.field {
  display: flex;
  flex-direction: column;
}
</style>
