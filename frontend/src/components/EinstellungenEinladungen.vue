<template>
  <BaseCard>
    <h5 class="text-lg font-semibold mb-4">Einladung senden</h5>
    <form @submit.prevent="onSubmit" class="grid grid-cols-1 gap-y-4 max-w-md">

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
          />
          <label for="rolleId">Benutzerrolle</label>
        </FloatLabel>
        <small v-if="errors.rolleId" class="p-error block">{{ errors.rolleId }}</small>
      </div>

      <!-- Verwaltung admin toggle -->
      <div v-if="isVerwaltung" class="flex items-center gap-x-3">
        <ToggleSwitch v-model="isVerwaltungAdmin" inputId="verwaltungAdmin" />
        <label for="verwaltungAdmin" class="text-sm">Admin-Rechte gewähren</label>
      </div>

      <div class="field">
        <template v-if="activeDomain">
          <label class="block text-sm text-gray-500 mb-1">E-Mail-Adresse</label>
          <InputGroup>
            <InputText
              id="email"
              v-model="emailLocal"
              placeholder="vorname.nachname"
              :invalid="!!errors.email"
              :disabled="!rolleId"
            />
            <InputGroupAddon>@{{ activeDomain }}</InputGroupAddon>
          </InputGroup>
        </template>
        <template v-else>
          <FloatLabel variant="on">
            <InputText
              id="email"
              v-model="email"
              class="w-full"
              :invalid="!!errors.email"
              :disabled="!rolleId"
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
        <small v-if="errors.gueltigStunden" class="p-error block">{{ errors.gueltigStunden }}</small>
      </div>

      <div v-if="isVerwaltung && isVerwaltungAdmin" class="flex items-center gap-2 text-sm text-gray-500">
        <i class="pi pi-info-circle" />
        Einladung als Verwaltung mit Admin-Rechten.
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
import { useAuthStore } from '@/stores/auth'
import { useToast } from 'openvue/usetoast'

const ADMIN_ROLLE_NAME = 'Admin'
const VERWALTUNG_ROLLE_NAME = 'Verwaltung'
const POLITIK_ROLLE_NAME = 'Politik'

const gueltigkeitsOptionen = [
  { label: '1 Stunde', value: 1 },
  { label: '3 Stunden', value: 3 },
  { label: '1 Tag', value: 24 },
  { label: '3 Tage', value: 72 },
  { label: '7 Tage', value: 168 },
]

const rolleOptions = ref([])
const verwaltungDomain = ref(null)
const isSubmitting = ref(false)
const isVerwaltungAdmin = ref(false)
const emailLocal = ref('')
const toast = useToast()
const authStore = useAuthStore()

const { defineField, handleSubmit, errors, resetForm, setFieldValue } = useForm({
  validationSchema: yup.object({
    email: yup.string().required('E-Mail ist erforderlich').email('Ungültige E-Mail-Adresse').label('E-Mail'),
    rolleId: yup.number().required('Rolle ist erforderlich').label('Rolle'),
    gueltigStunden: yup.number().required().label('Gültigkeitsdauer'),
  }),
  initialValues: { gueltigStunden: 72 },
})

const [email] = defineField('email')
const [rolleId] = defineField('rolleId')
const [gueltigStunden] = defineField('gueltigStunden')

onMounted(async () => {
  try {
    const [user, rRes] = await Promise.all([
      authStore.getUser(),
      apiClient.get('/option/user-rolle'),
    ])
    rolleOptions.value = rRes.data
    verwaltungDomain.value = user?.gemeinde?.verwaltungEmailDomain ?? null
  } catch { /* */ }
})

// Politik users can only invite other Politik users
const isPolitik = computed(() => authStore.effectiveRolleId === 2)

const availableRollen = computed(() => {
  if (isPolitik.value) {
    return rolleOptions.value.filter((r) => r.name === POLITIK_ROLLE_NAME)
  }
  return rolleOptions.value.filter((r) => r.name !== ADMIN_ROLLE_NAME)
})

const selectedRolle = computed(() =>
  rolleOptions.value.find((r) => r.id === rolleId.value)
)

const isVerwaltung = computed(() => selectedRolle.value?.name === VERWALTUNG_ROLLE_NAME)

// Only show domain-split input when role is Verwaltung and domain exists
const activeDomain = computed(() => (isVerwaltung.value ? verwaltungDomain.value : null))

watch(rolleId, () => {
  emailLocal.value = ''
  setFieldValue('email', '')
  isVerwaltungAdmin.value = false
})

watch([emailLocal, activeDomain], ([local, domain]) => {
  if (domain) {
    setFieldValue('email', local ? `${local}@${domain}` : '')
  }
})

const onSubmit = handleSubmit(async (values) => {
  isSubmitting.value = true
  try {
    await apiClient.post('/einstellungen/einladung', {
      email: values.email,
      rolle_id: values.rolleId,
      gueltig_stunden: values.gueltigStunden,
      is_local_superuser: isVerwaltung.value ? isVerwaltungAdmin.value : false,
    })
    toast.add({
      severity: 'success',
      summary: 'Einladung gesendet',
      detail: `Einladung an ${values.email} wurde gesendet.`,
      life: 4000,
    })
    emailLocal.value = ''
    isVerwaltungAdmin.value = false
    resetForm({ values: { gueltigStunden: 72 } })
  } catch {
    toast.add({
      severity: 'error',
      summary: 'Fehler',
      detail: 'Einladung konnte nicht gesendet werden.',
      life: 3000,
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
