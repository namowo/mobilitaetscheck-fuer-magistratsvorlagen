<template>
  <div>
    <BaseCard>
      <div class="flex items-center justify-between mb-3">
        <h5 class="text-lg font-semibold">Benutzer</h5>
        <InputText
          v-model="filters['global'].value"
          placeholder="Suchen…"
          size="small"
          class="w-56"
        />
      </div>
      <div class="flex gap-2 mb-3">
        <Select
          v-model="filterRolle"
          :options="rolleFilterOptions"
          optionLabel="name"
          optionValue="name"
          placeholder="Rolle"
          showClear
          size="small"
          class="w-36"
        />
        <Select
          v-model="filterGruppe"
          :options="gruppeFilterOptions"
          optionLabel="label"
          optionValue="value"
          placeholder="Gruppe"
          showClear
          size="small"
          class="w-40"
        />
      </div>

      <BaseSpinner v-if="isLoading" />
      <DataTable
        v-else
        :value="filteredUsers"
        :paginator="filteredUsers.length > 20"
        :rows="20"
        size="small"
        sortMode="single"
        v-model:filters="filters"
        :globalFilterFields="['vorname', 'nachname', 'email', 'rolle.name', 'gruppe.name']"
        class="w-full"
      >
        <template #empty>
          <span class="text-gray-400 text-sm">Keine Benutzer gefunden.</span>
        </template>
        <Column field="vorname" header="Vorname" sortable />
        <Column field="nachname" header="Nachname" sortable />
        <Column field="email" header="E-Mail" sortable />
        <Column field="rolle.name" header="Rolle" sortable>
          <template #body="{ data }">{{ data.rolle?.name }}</template>
        </Column>
        <Column field="gruppe.name" header="Gruppe" sortable>
          <template #body="{ data }">
            <span :class="data.gruppe ? '' : 'text-gray-400'">{{ data.gruppe?.name ?? '–' }}</span>
          </template>
        </Column>
        <Column header="Kommunaler Admin" style="width: 100px">
          <template #body="{ data }">
            <i v-if="data.isLocalSuperuser" class="pi pi-check text-green-600" />
          </template>
        </Column>
        <Column header="" style="width: 80px">
          <template #body="{ data }">
            <div class="flex gap-1">
              <Button icon="pi pi-pencil" text size="small" @click="openEdit(data)" />
              <Button icon="pi pi-trash" text size="small" severity="danger" :disabled="data.id === authStore.userId" @click="confirmDelete(data)" />
            </div>
          </template>
        </Column>
      </DataTable>
    </BaseCard>

    <Dialog v-model:visible="editVisible" header="Benutzer bearbeiten" :modal="true" class="w-full max-w-md">
      <div class="grid grid-cols-1 gap-y-4 mt-2">
        <div class="bg-gray-50 rounded-lg p-3 grid grid-cols-1 gap-y-1 text-sm">
          <div class="flex gap-2">
            <span class="text-gray-500 w-24 shrink-0">Name</span>
            <span class="font-medium">{{ editData.vorname }} {{ editData.nachname }}</span>
          </div>
          <div class="flex gap-2">
            <span class="text-gray-500 w-24 shrink-0">E-Mail</span>
            <span class="font-medium break-all">{{ editData.email }}</span>
          </div>
          <div class="flex gap-2">
            <span class="text-gray-500 w-24 shrink-0">Registriert</span>
            <span class="font-medium">{{ editData.erstelltAm }}</span>
          </div>
        </div>

        <div class="field">
          <FloatLabel variant="on">
            <Select
              id="editRolle"
              v-model="editData.rolle_id"
              :options="availableRollen"
              optionLabel="name"
              optionValue="id"
              class="w-full"
            />
            <label for="editRolle">Rolle</label>
          </FloatLabel>
        </div>
        <div class="field">
          <FloatLabel variant="on">
            <Select
              id="editGruppe"
              v-model="editData.gruppe_id"
              :options="[{ id: null, name: 'Keine Gruppe' }, ...gruppeOptions]"
              optionLabel="name"
              optionValue="id"
              class="w-full"
            />
            <label for="editGruppe">Gruppe</label>
          </FloatLabel>
        </div>
        <div class="flex items-center gap-x-3">
          <ToggleSwitch v-model="editData.is_local_superuser" inputId="is_local_superuser" />
          <label for="is_local_superuser" class="text-sm">Kommunaler Administrator</label>
        </div>
      </div>
      <template #footer>
        <Button label="Abbrechen" text @click="editVisible = false" />
        <Button label="Speichern" @click="saveEdit" :loading="isSaving" />
      </template>
    </Dialog>
  </div>
</template>

<script setup>
import { ref, onMounted, reactive, computed } from 'vue'
import { FilterMatchMode } from '@openvue/core/api'
import { useConfirm } from 'openvue/useconfirm'
import Button from 'openvue/button'
import DataTable from 'openvue/datatable'
import Column from 'openvue/column'
import Dialog from 'openvue/dialog'
import Select from 'openvue/select'
import FloatLabel from 'openvue/floatlabel'
import InputText from 'openvue/inputtext'
import ToggleSwitch from 'openvue/toggleswitch'
import { apiClient } from '@/services/axios'
import { useAuthStore } from '@/stores/auth'
import { useToast } from 'openvue/usetoast'

const ADMIN_ROLLE_NAME = 'Admin'

const authStore = useAuthStore()

const users = ref([])
const rolleOptions = ref([])
const isLoading = ref(false)
const editVisible = ref(false)
const isSaving = ref(false)
const gruppeOptions = ref([])
const editData = reactive({
  user_id: null,
  vorname: '',
  nachname: '',
  email: '',
  erstelltAm: '',
  rolle_id: null,
  gruppe_id: null,
  is_local_superuser: false,
})
const toast = useToast()
const confirm = useConfirm()

const filterRolle = ref(null)
const filterGruppe = ref(null)
const filters = ref({
  global: { value: null, matchMode: FilterMatchMode.CONTAINS },
})

// Exclude Admin role — Verwaltung admins cannot assign the Admin role
const availableRollen = computed(() =>
  rolleOptions.value.filter((r) => r.name !== ADMIN_ROLLE_NAME)
)

const rolleFilterOptions = computed(() =>
  [...new Map(users.value.map((u) => [u.rolle?.name, u.rolle]).filter(([n]) => n)).values()]
    .sort((a, b) => a.name.localeCompare(b.name))
)

const gruppeFilterOptions = computed(() => {
  const opts = [...new Map(
    users.value
      .filter((u) => u.gruppe)
      .map((u) => [u.gruppe.name, { label: u.gruppe.name, value: u.gruppe.name }])
  ).values()].sort((a, b) => a.label.localeCompare(b.label))
  return [{ label: 'Ohne Gruppe', value: '__none__' }, ...opts]
})

const filteredUsers = computed(() => {
  return users.value.filter((u) => {
    if (filterRolle.value && u.rolle?.name !== filterRolle.value) return false
    if (filterGruppe.value === '__none__' && u.gruppe) return false
    if (filterGruppe.value && filterGruppe.value !== '__none__' && u.gruppe?.name !== filterGruppe.value) return false
    return true
  })
})

onMounted(async () => {
  isLoading.value = true
  try {
    const [usersRes, rollenRes, gruppenRes] = await Promise.all([
      apiClient.get('/users'),
      apiClient.get('/option/user-rolle'),
      apiClient.get('/einstellungen/gruppe'),
    ])
    users.value = usersRes.data
    rolleOptions.value = rollenRes.data
    gruppeOptions.value = gruppenRes.data
  } catch { /* */ } finally {
    isLoading.value = false
  }
})

const openEdit = (user) => {
  editData.user_id = user.id
  editData.vorname = user.vorname
  editData.nachname = user.nachname
  editData.email = user.email
  editData.erstelltAm = user.erstelltAm
    ? new Date(user.erstelltAm).toLocaleDateString('de-DE', { day: '2-digit', month: '2-digit', year: 'numeric' })
    : '–'
  editData.rolle_id = user.rolleId
  editData.gruppe_id = user.gruppeId ?? null
  editData.is_local_superuser = user.isLocalSuperuser
  editVisible.value = true
}

const saveEdit = async () => {
  isSaving.value = true
  try {
    const res = await apiClient.patch(`/einstellungen/benutzer/${editData.user_id}`, {
      rolle_id: editData.rolle_id,
      gruppe_id: editData.gruppe_id,
      is_local_superuser: editData.is_local_superuser,
    })
    const idx = users.value.findIndex((u) => u.id === editData.user_id)
    if (idx !== -1) users.value[idx] = res.data
    if (editData.user_id === authStore.userId) {
      await authStore.refreshUser()
    }
    editVisible.value = false
    toast.add({ severity: 'success', summary: 'Gespeichert', life: 3000 })
  } catch {
    toast.add({ severity: 'error', summary: 'Fehler', detail: 'Änderung fehlgeschlagen', life: 3000 })
  } finally {
    isSaving.value = false
  }
}

const confirmDelete = (user) => {
  confirm.require({
    message: `Möchten Sie ${user.vorname} ${user.nachname} (${user.email}) wirklich löschen?`,
    header: 'Benutzer löschen',
    icon: 'pi pi-exclamation-triangle',
    rejectProps: { label: 'Abbrechen', severity: 'secondary', outlined: true },
    acceptProps: { label: 'Löschen', severity: 'danger' },
    accept: async () => {
      try {
        await apiClient.delete(`/einstellungen/benutzer/${user.id}`)
        users.value = users.value.filter((u) => u.id !== user.id)
        toast.add({ severity: 'success', summary: 'Benutzer gelöscht', life: 3000 })
      } catch {
        toast.add({ severity: 'error', summary: 'Fehler', detail: 'Benutzer konnte nicht gelöscht werden.', life: 3000 })
      }
    },
  })
}
</script>
