<template>
  <div>
    <BaseCard class="block mx-auto my-7 max-w-md">
      <h4 class="text-xl font-bold dark:text-white mb-1">Erstkonfiguration</h4>
      <p class="text-sm text-gray-500 mb-5">
        Legen Sie den Systemadministrator-Account an. Dieser Schritt ist nur einmalig möglich.
      </p>
      <BaseAlert
        v-if="errorMessage"
        type="error"
        title="Fehler"
        :message="errorMessage"
        class="mb-4"
      />
      <form @submit.prevent="onSubmit" class="grid grid-cols-1 gap-y-4">
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
        <div class="field">
          <FloatLabel variant="on">
            <InputText id="email" v-model="email" class="w-full" :invalid="!!errors.email" />
            <label for="email">E-Mail</label>
          </FloatLabel>
          <small v-if="errors.email" class="p-error block">{{ errors.email }}</small>
        </div>
        <div class="field">
          <FloatLabel variant="on">
            <Password
              id="password"
              v-model="password"
              class="w-full"
              inputClass="w-full"
              toggleMask
              :feedback="false"
              :invalid="!!errors.password"
            />
            <label for="password">Passwort</label>
          </FloatLabel>
          <small v-if="errors.password" class="p-error block">{{ errors.password }}</small>
        </div>
        <div class="field">
          <FloatLabel variant="on">
            <Password
              id="confirmPassword"
              v-model="confirmPassword"
              class="w-full"
              inputClass="w-full"
              toggleMask
              :feedback="false"
              :invalid="!!errors.confirmPassword"
            />
            <label for="confirmPassword">Passwort wiederholen</label>
          </FloatLabel>
          <small v-if="errors.confirmPassword" class="p-error block">{{
            errors.confirmPassword
          }}</small>
        </div>
        <Button label="Systemadministrator anlegen" type="submit" class="w-full" :loading="isLoading" />
      </form>
    </BaseCard>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useForm } from 'vee-validate'
import { schema } from '@/utils/schemas/setup'
import { apiClient } from '@/services/axios'
import { resetSetupStatus } from '@/router'
import InputText from 'openvue/inputtext'
import FloatLabel from 'openvue/floatlabel'
import Password from 'openvue/password'
import Button from 'openvue/button'

const router = useRouter()
const isLoading = ref(false)
const errorMessage = ref(null)

const { defineField, handleSubmit, errors } = useForm({ validationSchema: schema })

const [vorname] = defineField('vorname')
const [nachname] = defineField('nachname')
const [email] = defineField('email')
const [password] = defineField('password')
const [confirmPassword] = defineField('confirmPassword')

const onSubmit = handleSubmit(async (values) => {
  isLoading.value = true
  errorMessage.value = null
  try {
    await apiClient.post('/public/setup', {
      vorname: values.vorname,
      nachname: values.nachname,
      email: values.email,
      password: values.password
    })
    resetSetupStatus()
    router.push({ name: 'anmelden' })
  } catch (error) {
    errorMessage.value =
      error?.response?.data?.detail ?? 'Ein Fehler ist aufgetreten. Bitte versuchen Sie es erneut.'
  } finally {
    isLoading.value = false
  }
})
</script>
