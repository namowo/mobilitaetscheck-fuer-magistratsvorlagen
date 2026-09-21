<template>
  <BaseCard>
    <h5 class="text-lg font-semibold mb-4">Einladung senden</h5>
    <form @submit.prevent="onSubmit" class="grid grid-cols-1 gap-y-4 max-w-md">
      <div class="field">
        <FloatLabel variant="on">
          <Select
            id="gemeindeId"
            v-model="gemeindeId"
            :options="gemeindeOptions"
            optionLabel="name"
            optionValue="id"
            class="w-full"
            :invalid="!!errors.gemeindeId"
          />
          <label for="gemeindeId">Kommune</label>
        </FloatLabel>
        <small v-if="errors.gemeindeId" class="p-error block">{{ errors.gemeindeId }}</small>
      </div>

      <div class="field">
        <FloatLabel variant="on">
          <Select
            id="rolleId"
            v-model="rolleId"
            :options="availableRollen"
            optionLabel="name"
            optionValue="id"
            class="w-full"
            :invalid="!!errors.rolleId"
            :disabled="isSystemadministration"
          />
          <label for="rolleId">Benutzerrolle</label>
        </FloatLabel>
        <small v-if="errors.rolleId" class="p-error block">{{ errors.rolleId }}</small>
      </div>

      <!-- Verwaltung admin toggle -->
      <div v-if="isVerwaltung" class="flex items-center gap-x-3">
        <ToggleSwitch v-model="isVerwaltungAdmin" inputId="verwaltungAdmin" />
        <label for="verwaltungAdmin" class="text-sm">Als kommunaler Administrator einladen</label>
      </div>

      <div class="field">
        <template v-if="verwaltungDomain">
          <label class="block text-sm text-gray-500 mb-1">E-Mail-Adresse</label>
          <InputGroup>
            <InputText
              id="email"
              v-model="emailLocal"
              placeholder="vorname.nachname"
              :invalid="!!errors.email"
              :disabled="!gemeindeId || !rolleId"
            />
            <InputGroupAddon>@{{ verwaltungDomain }}</InputGroupAddon>
          </InputGroup>
        </template>
        <template v-else>
          <FloatLabel variant="on">
            <InputText
              id="email"
              v-model="email"
              class="w-full"
              :invalid="!!errors.email"
              :disabled="!gemeindeId || !rolleId"
            />
            <label for="email">E-Mail-Adresse</label>
          </FloatLabel>
        </template>
        <small v-if="errors.email" class="p-error block">{{ errors.email }}</small>
      </div>

      <div class="field">
        <FloatLabel variant="on">
          <Select
            id="gueltigStunden"
            v-model="gueltigStunden"
            :options="gueltigkeitsOptionen"
            optionLabel="label"
            optionValue="value"
            class="w-full"
            :invalid="!!errors.gueltigStunden"
          />
          <label for="gueltigStunden">Gültigkeitsdauer</label>
        </FloatLabel>
        <small v-if="errors.gueltigStunden" class="p-error block">{{
          errors.gueltigStunden
        }}</small>
      </div>

      <!-- Role hint -->
      <div v-if="roleHint" class="flex items-center gap-2 text-sm text-gray-500">
        <i class="pi pi-info-circle" />
        {{ roleHint }}
      </div>

      <Button label="Einladung senden" type="submit" :loading="isSubmitting" class="w-fit" />
    </form>
  </BaseCard>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import { useForm } from 'vee-validate'
import * as yup from 'yup'
import Button from 'openvue/button'
import InputText from 'openvue/inputtext'
import FloatLabel from 'openvue/floatlabel'
import InputGroup from 'openvue/inputgroup'
import InputGroupAddon from 'openvue/inputgroupaddon'
import Select from 'openvue/select'
import ToggleSwitch from 'openvue/toggleswitch'
import { apiClient } from '@/services/axios'
import { useToast } from 'openvue/usetoast'

const SYSTEM_GEMEINDE_NAME = 'Systemadministration'
const ADMIN_ROLLE_NAME = 'Admin'
const VERWALTUNG_ROLLE_NAME = 'Verwaltung'

const gueltigkeitsOptionen = [
  { label: '1 Stunde', value: 1 },
  { label: '3 Stunden', value: 3 },
  { label: '1 Tag', value: 24 },
  { label: '3 Tage', value: 72 },
  { label: '7 Tage', value: 168 }
]

const gemeindeOptions = ref([])
const rolleOptions = ref([])
const isSubmitting = ref(false)
const isVerwaltungAdmin = ref(true)
const emailLocal = ref('')
const toast = useToast()

const { defineField, handleSubmit, errors, resetForm, setFieldValue } = useForm({
  validationSchema: yup.object({
    email: yup
      .string()
      .required('E-Mail ist erforderlich')
      .email('Ungültige E-Mail-Adresse')
      .label('E-Mail'),
    gemeindeId: yup.number().required('Kommune ist erforderlich').label('Kommune'),
    rolleId: yup.number().required('Rolle ist erforderlich').label('Rolle'),
    gueltigStunden: yup.number().required().label('Gültigkeitsdauer')
  }),
  initialValues: { gueltigStunden: 72 }
})

const [email] = defineField('email')
const [gemeindeId] = defineField('gemeindeId')
const [rolleId] = defineField('rolleId')
const [gueltigStunden] = defineField('gueltigStunden')

onMounted(async () => {
  try {
    const [gRes, rRes] = await Promise.all([
      apiClient.get('/admin/gemeinde'),
      apiClient.get('/option/user-rolle')
    ])
    gemeindeOptions.value = gRes.data
    rolleOptions.value = rRes.data
  } catch {
    /* */
  }
})

const selectedGemeinde = computed(() =>
  gemeindeOptions.value.find((g) => g.id === gemeindeId.value)
)

const isSystemadministration = computed(() => selectedGemeinde.value?.name === SYSTEM_GEMEINDE_NAME)

const availableRollen = computed(() => {
  if (isSystemadministration.value) {
    return rolleOptions.value.filter((r) => r.name === ADMIN_ROLLE_NAME)
  }
  return rolleOptions.value.filter((r) => r.name !== ADMIN_ROLLE_NAME)
})

const selectedRolle = computed(() => rolleOptions.value.find((r) => r.id === rolleId.value))

const isVerwaltung = computed(() => selectedRolle.value?.name === VERWALTUNG_ROLLE_NAME)

const verwaltungDomain = computed(() => {
  if (!isVerwaltung.value) return null
  return selectedGemeinde.value?.verwaltungEmailDomain || null
})

// Fix Select-close bug: use watch instead of @change
watch(gemeindeId, () => {
  emailLocal.value = ''
  setFieldValue('email', '')
  if (isSystemadministration.value) {
    const adminRolle = rolleOptions.value.find((r) => r.name === ADMIN_ROLLE_NAME)
    if (adminRolle) setFieldValue('rolleId', adminRolle.id)
  } else if (selectedRolle.value?.name === ADMIN_ROLLE_NAME) {
    setFieldValue('rolleId', undefined)
  }
})

watch(rolleId, () => {
  emailLocal.value = ''
  setFieldValue('email', '')
  isVerwaltungAdmin.value = true
})

watch([emailLocal, verwaltungDomain], ([local, domain]) => {
  if (domain) {
    setFieldValue('email', local ? `${local}@${domain}` : '')
  }
})

const derivedIsSuperuser = computed(() => {
  if (isSystemadministration.value) return true
  if (isVerwaltung.value) return isVerwaltungAdmin.value
  return false
})

const roleHint = computed(() => {
  if (isSystemadministration.value) return 'Einladung als Systemadministrator.'
  if (isVerwaltung.value && isVerwaltungAdmin.value)
    return 'Einladung als kommunaler Administrator (Verwaltung mit Admin-Rechten).'
  return null
})

const onSubmit = handleSubmit(async (values) => {
  isSubmitting.value = true
  try {
    await apiClient.post('/einstellungen/einladung', {
      email: values.email,
      rolle_id: values.rolleId,
      gueltig_stunden: values.gueltigStunden,
      gemeinde_id: values.gemeindeId,
      is_superuser: derivedIsSuperuser.value
    })
    toast.add({
      severity: 'success',
      summary: 'Einladung gesendet',
      detail: `Einladung an ${values.email} wurde gesendet.`,
      life: 4000
    })
    emailLocal.value = ''
    isVerwaltungAdmin.value = true
    resetForm({ values: { gueltigStunden: 72 } })
  } catch {
    toast.add({
      severity: 'error',
      summary: 'Fehler',
      detail: 'Einladung konnte nicht gesendet werden.',
      life: 3000
    })
  } finally {
    isSubmitting.value = false
  }
})
</script>

<style scoped>
.p-error {
  color: rgb(220 38 38);
  font-size: 0.875rem;
}
</style>
