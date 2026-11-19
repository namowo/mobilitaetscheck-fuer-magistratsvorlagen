<template>
  <div class="flex flex-col gap-6">
    <!-- Übersicht -->
    <section class="rounded-xl border border-gray-200 bg-white p-5">
      <div v-if="isLoading" class="flex items-center gap-4">
        <Skeleton shape="circle" size="4rem" />
        <div class="flex flex-1 flex-col gap-2">
          <Skeleton width="12rem" height="1.25rem" />
          <Skeleton width="16rem" height="1rem" />
        </div>
      </div>
      <div v-else class="flex flex-wrap items-center gap-4">
        <Avatar
          :label="initialien"
          shape="circle"
          size="xlarge"
          class="shrink-0 !bg-blue-100 !text-blue-700 font-semibold"
        />
        <div class="min-w-0 flex-1">
          <p class="text-lg font-semibold text-gray-900 break-words">{{ anzeigeName }}</p>
          <p class="text-sm text-gray-600 break-all">{{ gespeicherteEmail }}</p>
          <div class="mt-2 flex flex-wrap gap-2">
            <Tag severity="secondary" icon="pi pi-building" :value="gemeindeName" />
            <Tag severity="secondary" icon="pi pi-id-card" :value="rolleName" />
          </div>
        </div>
      </div>
    </section>

    <!-- Persönliche Angaben -->
    <section class="rounded-xl border border-gray-200 bg-white p-5">
      <div class="mb-5 flex items-start gap-3">
        <span
          class="flex h-9 w-9 shrink-0 items-center justify-center rounded-lg bg-blue-100 text-blue-700"
        >
          <i class="pi pi-user" />
        </span>
        <div>
          <h4 class="font-semibold text-gray-900">Persönliche Angaben</h4>
          <p class="text-sm text-gray-600">
            Kommune und Rolle werden von der Verwaltung festgelegt und können hier nicht geändert
            werden.
          </p>
        </div>
      </div>

      <BaseSkeleton v-if="isLoading" variant="form" :rows="3" />
      <form v-else @submit.prevent="onSubmit" class="grid grid-cols-1 gap-4 sm:grid-cols-2">
        <div class="field">
          <FloatLabel variant="on">
            <InputText id="vorname" v-model="vorname" class="w-full" :invalid="!!errors.vorname" />
            <label for="vorname">Vorname</label>
          </FloatLabel>
          <small v-if="errors.vorname" class="p-error block">{{ errors.vorname }}</small>
        </div>

        <div class="field">
          <FloatLabel variant="on">
            <InputText
              id="nachname"
              v-model="nachname"
              class="w-full"
              :invalid="!!errors.nachname"
            />
            <label for="nachname">Nachname</label>
          </FloatLabel>
          <small v-if="errors.nachname" class="p-error block">{{ errors.nachname }}</small>
        </div>

        <!-- Email: only for Politik and Admin -->
        <div v-if="canEditEmail" class="field sm:col-span-2">
          <FloatLabel variant="on">
            <InputText id="email" v-model="email" class="w-full" :invalid="!!errors.email" />
            <label for="email">E-Mail</label>
          </FloatLabel>
          <small v-if="errors.email" class="p-error block">{{ errors.email }}</small>
        </div>

        <!-- Gruppe: for Verwaltung and Politik -->
        <div v-if="canEditGruppe" class="field sm:col-span-2">
          <FloatLabel variant="on">
            <Select
              id="gruppeId"
              v-model="gruppeId"
              :options="gruppenOptions"
              optionLabel="name"
              optionValue="id"
              class="w-full"
              showClear
              filter
              :filterFields="['name']"
              @filter="onGruppeFilter"
              @hide="gruppeFilterValue = ''"
              :loading="isCreatingGruppe"
            >
              <template #emptyfilter>
                <div
                  v-if="canCreateGruppe"
                  class="cursor-pointer px-2 py-1 hover:bg-gray-100 rounded"
                  @click="createGruppeInline"
                >
                  + {{ gruppeFilterValue }}
                </div>
                <span v-else>Keine Ergebnisse gefunden.</span>
              </template>
            </Select>
            <label for="gruppeId">{{ gruppeLabel }} <LabelOptional /></label>
          </FloatLabel>
        </div>

        <div class="flex justify-end sm:col-span-2">
          <Button type="submit" label="Speichern" icon="pi pi-save" :loading="isSaving" />
        </div>
      </form>
    </section>
  </div>
</template>

<script setup>
import { onMounted, ref, computed } from 'vue'
import { useAuthStore } from '@/stores/auth'
import { schema } from '@/utils/schemas/accountDaten.js'
import { useForm } from 'vee-validate'
import { useToast } from 'openvue/usetoast'
import FloatLabel from 'openvue/floatlabel'
import InputText from 'openvue/inputtext'
import Select from 'openvue/select'
import { apiClient } from '@/services/axios'
import Button from 'openvue/button'
import Avatar from 'openvue/avatar'
import Tag from 'openvue/tag'
import Skeleton from 'openvue/skeleton'

const isLoading = ref(true)
const isSaving = ref(false)
const gespeicherteEmail = ref('')
const gespeicherterName = ref({ vorname: '', nachname: '' })
const gemeindeName = ref('')
const rolleName = ref('')
const userRolleName = ref('')
const gruppen = ref([])
const gruppeFilterValue = ref('')
const isCreatingGruppe = ref(false)

const isVerwaltung = computed(() => userRolleName.value === 'Verwaltung')
const isPolitik = computed(() => userRolleName.value === 'Politik')
const canEditGruppe = computed(() => isVerwaltung.value || isPolitik.value)
const canCreateGruppe = computed(() => isPolitik.value && gruppeFilterValue.value.trim().length > 0)
const canEditEmail = computed(() => ['Politik', 'Admin'].includes(userRolleName.value))
const initialien = computed(() =>
  `${gespeicherterName.value.vorname?.charAt(0) ?? ''}${gespeicherterName.value.nachname?.charAt(0) ?? ''}`.toUpperCase()
)
const anzeigeName = computed(() =>
  `${gespeicherterName.value.vorname ?? ''} ${gespeicherterName.value.nachname ?? ''}`.trim()
)
const gruppeLabel = computed(() => 'Gruppe')
const gruppenOptions = computed(() => [
  { id: null, name: 'Keine Gruppe' },
  ...gruppen.value
])

const onGruppeFilter = (event) => {
  gruppeFilterValue.value = event.value
}

const { defineField, handleSubmit, errors, setFieldValue } = useForm({
  validationSchema: schema
})

const [email] = defineField('email')
const [vorname] = defineField('vorname')
const [nachname] = defineField('nachname')
const [gruppeId] = defineField('gruppeId')

const authStore = useAuthStore()
const toast = useToast()

const createGruppeInline = async () => {
  const name = gruppeFilterValue.value.trim()
  if (!name || isCreatingGruppe.value) return
  isCreatingGruppe.value = true
  try {
    const res = await apiClient.post('/einstellungen/gruppe/eigene', { name })
    gruppen.value = [...gruppen.value, res.data].sort((a, b) => a.name.localeCompare(b.name))
    setFieldValue('gruppeId', res.data.id)
    gruppeFilterValue.value = ''
    toast.add({ severity: 'success', summary: 'Gruppe erstellt', life: 3000 })
  } catch {
    toast.add({ severity: 'error', summary: 'Fehler beim Erstellen der Gruppe', life: 3000 })
  } finally {
    isCreatingGruppe.value = false
  }
}

onMounted(async () => {
  try {
    const [userRes, gemeindenRes, rollenRes] = await Promise.all([
      authStore.getUser(),
      apiClient.get('/option/gemeinde'),
      apiClient.get('/option/user-rolle')
    ])
    setFieldValue('email', userRes.email)
    setFieldValue('vorname', userRes.vorname)
    setFieldValue('nachname', userRes.nachname)
    setFieldValue('gruppeId', userRes.gruppeId ?? null)
    gespeicherteEmail.value = userRes.email
    gespeicherterName.value = { vorname: userRes.vorname, nachname: userRes.nachname }

    const g = gemeindenRes.data.find((g) => g.id === userRes.gemeindeId)
    const r = rollenRes.data.find((r) => r.id === userRes.rolleId)
    gemeindeName.value = g?.name ?? '–'
    rolleName.value = r?.name ?? '–'
    userRolleName.value = r?.name ?? ''

    if (isVerwaltung.value) {
      const gruppenRes = await apiClient.get('/einstellungen/gruppe')
      gruppen.value = gruppenRes.data.filter((g) => g.rolleId === userRes.rolleId)
    } else if (isPolitik.value) {
      const gruppenRes = await apiClient.get('/public/gruppen', {
        params: { gemeinde_id: userRes.gemeindeId, rolle_id: userRes.rolleId }
      })
      gruppen.value = gruppenRes.data
    }
  } catch {
    /* */
  } finally {
    isLoading.value = false
  }
})

const onSubmit = handleSubmit(async (values) => {
  isSaving.value = true
  try {
    const updateData = { vorname: values.vorname, nachname: values.nachname }
    if (canEditEmail.value) updateData.email = values.email
    await authStore.updateUser(updateData)

    if (canEditGruppe.value) {
      await apiClient.patch('/users/me/gruppe', { gruppe_id: values.gruppeId ?? null })
    }

    gespeicherterName.value = { vorname: values.vorname, nachname: values.nachname }
    if (canEditEmail.value) gespeicherteEmail.value = values.email
    toast.add({ severity: 'success', summary: 'Profil aktualisiert', life: 3000 })
  } catch {
    toast.add({ severity: 'error', summary: 'Fehler beim Aktualisieren', life: 3000 })
  } finally {
    isSaving.value = false
  }
})
</script>
