<template>
  <BaseSpinner v-if="isLoading" />
  <div v-else>
    <template v-if="kommuneNichtDabei && kontaktEmail">
      <Message severity="info" class="text-left">
        Ihre Kommune ist noch nicht Teil des Mobilitätschecks. Bitte senden Sie uns eine Anfrage,
        damit wir Ihre Kommune für die Politik freischalten können.
      </Message>
      <div class="flex justify-between mt-4">
        <Button label="Zurück" severity="secondary" icon="pi pi-arrow-left" @click="$emit('zurueck')" />
        <Button as="a" :href="mailtoHref" label="Nachricht senden" icon="pi pi-envelope" />
      </div>
    </template>

    <form v-else @submit.prevent="onSubmit" class="grid grid-cols-1 gap-y-4 mt-4">
      <div class="field">
        <FloatLabel variant="on">
          <Select
            id="gruppeId"
            v-model="gruppeId"
            :options="gruppenOptionen"
            optionLabel="name"
            optionValue="id"
            class="w-full"
            showClear
          />
          <label for="gruppeId">Gruppe (optional)</label>
        </FloatLabel>
      </div>

      <div class="field">
        <FloatLabel variant="on">
          <InputText
            id="vorname"
            v-model="vorname"
            class="w-full"
            :invalid="!!errors.vorname"
            aria-describedby="vorname-help"
          />
          <label for="vorname">Vorname</label>
        </FloatLabel>
        <small v-if="errors.vorname" id="vorname-help" class="p-error block">{{
          errors.vorname
        }}</small>
      </div>

      <div class="field">
        <FloatLabel variant="on">
          <InputText
            id="nachname"
            v-model="nachname"
            class="w-full"
            :invalid="!!errors.nachname"
            aria-describedby="nachname-help"
          />
          <label for="nachname">Nachname</label>
        </FloatLabel>
        <small v-if="errors.nachname" id="nachname-help" class="p-error block">{{
          errors.nachname
        }}</small>
      </div>

      <div class="field">
        <FloatLabel variant="on">
          <InputText
            id="email"
            v-model="email"
            class="w-full"
            :invalid="!!errors.email"
            aria-describedby="email-help"
          />
          <label for="email">E-Mail</label>
        </FloatLabel>
        <small v-if="errors.email" id="email-help" class="p-error block">{{ errors.email }}</small>
      </div>

      <div class="field">
        <FloatLabel variant="on">
          <Password
            id="password"
            class="w-full"
            inputClass="w-full"
            v-model="password"
            promptLabel="Mindestanforderungen:"
            toggleMask
            :invalid="!!errors.password"
            aria-describedby="password-help"
          >
            <template #header>
              <h5 class="text-lg font-bold">Passwortstärke</h5>
            </template>
            <template #footer>
              <Divider />
              <ul class="pl-2 ml-2 my-0 leading-normal list-disc">
                <li>Mindestens einen Kleinbuchstaben</li>
                <li>Mindestens einen Großbuchstaben</li>
                <li>Mindestens eine Ziffer</li>
                <li>Mindestens ein Sonderzeichen</li>
                <li>Mindestens 8 Zeichen</li>
              </ul>
            </template>
          </Password>
          <label for="password">Passwort</label>
        </FloatLabel>
        <small v-if="errors.password" id="password-help" class="p-error block">{{
          errors.password
        }}</small>
      </div>

      <div class="field">
        <FloatLabel variant="on">
          <Password
            id="confirmPassword"
            class="w-full"
            inputClass="w-full"
            v-model="confirmPassword"
            toggleMask
            :feedback="false"
            :invalid="!!errors.confirmPassword"
            aria-describedby="confirmPassword-help"
          />
          <label for="confirmPassword">Passwort wiederholen</label>
        </FloatLabel>
        <small v-if="errors.confirmPassword" id="confirmPassword-help" class="p-error block">{{
          errors.confirmPassword
        }}</small>
      </div>

      <DatenschutzZustimmung v-model="datenschutzAkzeptiert" :error-message="errors.datenschutzAkzeptiert" />
      <NutzungsbedingungenZustimmung
        v-model="nutzungsbedingungenAkzeptiert"
        :error-message="errors.nutzungsbedingungenAkzeptiert"
      />
      <WeitereZustimmung
        v-model="weitereZustimmungAkzeptiert"
        :error-message="errors.weitereZustimmungAkzeptiert"
      />

      <div class="flex justify-between">
        <Button label="Zurück" severity="secondary" icon="pi pi-arrow-left" @click="$emit('zurueck')" />
        <Button label="Registrieren" type="submit" />
      </div>
    </form>
  </div>
</template>

<script setup>
import { ref, watch, onMounted } from 'vue'
import { useAuthStore } from '@/stores/auth'
import { useRouter } from 'vue-router'
import { useForm } from 'vee-validate'
import { schema } from '@/utils/schemas/authRegistrieren'
import Button from 'openvue/button'
import InputText from 'openvue/inputtext'
import FloatLabel from 'openvue/floatlabel'
import Password from 'openvue/password'
import Divider from 'openvue/divider'
import Select from 'openvue/select'
import Message from 'openvue/message'
import DatenschutzZustimmung from '@/components/DatenschutzZustimmung.vue'
import NutzungsbedingungenZustimmung from '@/components/NutzungsbedingungenZustimmung.vue'
import WeitereZustimmung from '@/components/WeitereZustimmung.vue'
import { apiClient } from '@/services/axios'
import { useToast } from 'openvue/usetoast'
import { useKommuneAnfrageMailto } from '@/composables/kommuneAnfrageMailto'

const props = defineProps({
  gemeindeId: { type: [Number, String], default: null },
  kommuneNichtDabei: { type: Boolean, default: false }
})
defineEmits(['zurueck'])

const { kontaktEmail, mailtoHref, fetchVorlage } = useKommuneAnfrageMailto('politik')

const isLoading = ref(false)
const gruppenOptionen = ref([])
const gruppeId = ref(null)
const politikRolleId = ref(null)

const toast = useToast()
const router = useRouter()
const { register } = useAuthStore()

const { defineField, handleSubmit, errors, setFieldValue } = useForm({ validationSchema: schema })

const [vorname] = defineField('vorname')
const [nachname] = defineField('nachname')
const [email] = defineField('email')
const [password] = defineField('password')
const [confirmPassword] = defineField('confirmPassword')
const [datenschutzAkzeptiert] = defineField('datenschutzAkzeptiert')
const [nutzungsbedingungenAkzeptiert] = defineField('nutzungsbedingungenAkzeptiert')
const [weitereZustimmungAkzeptiert] = defineField('weitereZustimmungAkzeptiert')

setFieldValue('gemeindeId', props.kommuneNichtDabei ? null : props.gemeindeId)

onMounted(async () => {
  try {
    const rollenRes = await apiClient.get('/option/user-rolle')
    politikRolleId.value = rollenRes.data.find((r) => r.name === 'Politik')?.id ?? null
  } catch {
    politikRolleId.value = null
  }
  fetchVorlage()
  await fetchGruppen(props.gemeindeId)
})

const fetchGruppen = async (gemeindeIdWert) => {
  gruppeId.value = null
  gruppenOptionen.value = []
  if (!gemeindeIdWert || props.kommuneNichtDabei || !politikRolleId.value) return
  try {
    const res = await apiClient.get('/public/gruppen', {
      params: { gemeinde_id: gemeindeIdWert, rolle_id: politikRolleId.value }
    })
    gruppenOptionen.value = res.data
  } catch {
    gruppenOptionen.value = []
  }
}

watch(
  () => props.gemeindeId,
  (newId) => {
    setFieldValue('gemeindeId', props.kommuneNichtDabei ? null : newId)
    fetchGruppen(newId)
  }
)

const onSubmit = handleSubmit(async (values) => {
  try {
    isLoading.value = true
    // eslint-disable-next-line no-unused-vars
    const { datenschutzAkzeptiert, nutzungsbedingungenAkzeptiert, weitereZustimmungAkzeptiert, ...registerValues } =
      values
    await register({ ...registerValues, rolle_id: 2, gruppeId: gruppeId.value ?? undefined })
    router.replace({
      name: 'account-bestaetigen',
      query: { verify: 'check-mail', email: values.email }
    })
  } catch (error) {
    console.log(error)
    toast.add({
      severity: 'error',
      summary: 'Fehler',
      detail: 'Registrierung fehlgeschlagen',
      life: 3000
    })
  } finally {
    isLoading.value = false
  }
})
</script>

<style scoped>
.p-error {
  @apply text-red-600;
}
</style>
