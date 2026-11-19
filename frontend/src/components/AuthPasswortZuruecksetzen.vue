<template>
  <div>
    <component
      :is="changePassword ? 'section' : BaseCard"
      :class="changePassword ? 'rounded-xl border border-gray-200 bg-white p-5' : ''"
    >
      <div v-if="changePassword" class="mb-5 flex items-start gap-3">
        <span
          class="flex h-9 w-9 shrink-0 items-center justify-center rounded-lg bg-blue-100 text-blue-700"
        >
          <i class="pi pi-lock" />
        </span>
        <div>
          <h4 class="font-semibold text-gray-900">Passwort ändern</h4>
          <p class="text-sm text-gray-600">
            Nach dem Ändern melden Sie sich beim nächsten Mal mit dem neuen Passwort an.
          </p>
        </div>
      </div>
      <h4 v-else class="text-xl font-bold dark:text-white mb-4">{{ label }}</h4>
      <form
        @submit.prevent="onSubmit"
        class="grid grid-cols-1 gap-4"
        :class="{ 'sm:grid-cols-2': changePassword }"
      >
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
        <div class="flex" :class="changePassword ? 'justify-end sm:col-span-2' : ''">
          <Button
            type="submit"
            :label="label"
            :icon="changePassword ? 'pi pi-lock' : undefined"
            :class="{ 'w-full': !changePassword }"
            :loading="isLoading"
          />
        </div>
      </form>
    </component>
  </div>
</template>

<script setup>
import { computed, ref } from 'vue'
import { useAuthStore } from '@/stores/auth'
import { useRoute, useRouter } from 'vue-router'
import { useForm } from 'vee-validate'
import { schema } from '@/utils/schemas/authPasswortZuruecksetzen.js'

import BaseCard from '@/components/BaseCard.vue'
import Button from 'openvue/button'
import FloatLabel from 'openvue/floatlabel'
import Password from 'openvue/password'
import Divider from 'openvue/divider'
import { useToast } from 'openvue/usetoast'

const isLoading = ref(false)

const props = defineProps({
  changePassword: {
    type: Boolean,
    default: false
  }
})

const label = computed(() => (props.changePassword ? 'Passwort ändern' : 'Passwort zurücksetzen'))

// Form setup
const { defineField, handleSubmit, errors, resetForm } = useForm({
  validationSchema: schema
})

const [password] = defineField('password')
const [confirmPassword] = defineField('confirmPassword')

const router = useRouter()
const route = useRoute()
const { updateUser, resetPassword } = useAuthStore()

const toast = useToast()

const onSubmit = handleSubmit(async (values) => {
  try {
    isLoading.value = true
    if (props.changePassword) {
      await updateUser(values)
      resetForm()
      isLoading.value = false
      toast.add({ severity: 'success', summary: 'Passwort geändert', life: 3000 })
    } else {
      const token = route.query.token
      const password = values.password
      await resetPassword(token, password)
      isLoading.value = false
      router.replace({ name: 'anmelden' })
      toast.add({
        severity: 'success',
        summary: 'Passwort erfolgreich geändert',
        life: 3000
      })
    }
  } catch (error) {
    isLoading.value = false
    toast.add({
      severity: 'error',
      summary: 'Fehler beim Ändern des Passworts',
      life: 3000
    })
  }
})
</script>

<style scoped>
.p-button {
  text-decoration: none;
}

.p-invalid {
  @apply border-red-600;
}

.p-error {
  @apply text-red-600;
}
</style>
