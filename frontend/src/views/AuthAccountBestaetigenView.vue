<template>
  <div>
  <div class="flex items-start justify-center pt-16 px-4">
    <div class="w-full max-w-md">

      <!-- check-mail state -->
      <div v-if="route.query.verify === 'check-mail'" class="text-center">
        <div class="flex justify-center mb-6">
          <div class="w-20 h-20 rounded-full bg-blue-100 flex items-center justify-center">
            <i class="pi pi-envelope text-blue-600" style="font-size: 2.25rem" />
          </div>
        </div>
        <h2 class="text-2xl font-bold text-gray-800 mb-3">E-Mail gesendet!</h2>
        <p class="text-gray-600 mb-6">
          Bitte klicken Sie auf den Link in der E-Mail, um Ihren Account zu aktivieren.
        </p>

        <!-- email display + edit -->
        <div v-if="currentEmail" class="bg-gray-50 border border-gray-200 rounded-lg px-4 py-3 mb-6 text-left">
          <p class="text-xs text-gray-500 mb-0.5">Hinterlegte E-Mail-Adresse</p>
          <div class="flex items-center justify-between gap-2">
            <p class="text-sm font-medium text-gray-800 break-all">{{ currentEmail }}</p>
            <Button
              icon="pi pi-pencil"
              text
              rounded
              size="small"
              aria-label="E-Mail-Adresse bearbeiten"
              @click="openEmailDialog"
            />
          </div>
        </div>

        <Message severity="info" class="mb-6 text-left">
          Keine E-Mail erhalten? Bitte prüfen Sie auch Ihren Spam-Ordner oder fordern Sie eine neue Bestätigungs-E-Mail an.
        </Message>

        <Message v-if="successMessage" severity="success" class="mb-6 text-left">
          {{ successMessage }}
        </Message>

        <Button
          label="Bestätigungs-E-Mail erneut senden"
          icon="pi pi-send"
          class="w-full mb-4"
          :loading="resendLoading"
          :disabled="!currentEmail || cooldown > 0"
          @click="resendVerification"
        />
        <p v-if="cooldown > 0" class="text-sm text-gray-500 mb-4">
          Erneut senden möglich in {{ cooldown }} Sekunden
        </p>

        <RouterLink :to="{ name: 'anmelden' }" class="text-sm text-blue-600 hover:underline">
          Zurück zur Anmeldung
        </RouterLink>
      </div>

      <!-- success state -->
      <div v-else-if="route.query.verify === 'success'" class="text-center">
        <div class="flex justify-center mb-6">
          <div class="w-20 h-20 rounded-full bg-green-100 flex items-center justify-center">
            <i class="pi pi-check text-green-600" style="font-size: 2.25rem" />
          </div>
        </div>
        <h2 class="text-2xl font-bold text-gray-800 mb-3">Account bestätigt!</h2>
        <p class="text-gray-600 mb-8">
          Ihr Account wurde erfolgreich bestätigt. Sie können sich jetzt anmelden.
        </p>
        <RouterLink :to="{ name: 'anmelden' }">
          <Button label="Jetzt anmelden" icon="pi pi-sign-in" class="w-full" />
        </RouterLink>
      </div>

      <!-- error state -->
      <div v-else-if="verifyError" class="text-center">
        <div class="flex justify-center mb-6">
          <div class="w-20 h-20 rounded-full bg-red-100 flex items-center justify-center">
            <i class="pi pi-times-circle text-red-500" style="font-size: 2.25rem" />
          </div>
        </div>
        <h2 class="text-2xl font-bold text-gray-800 mb-3">Link ungültig</h2>
        <p class="text-gray-600 mb-6">
          Der Bestätigungslink ist ungültig oder abgelaufen.
        </p>
        <Message severity="info" class="mb-6 text-left">
          Fordern Sie einen neuen Link an, indem Sie sich anmelden oder unten Ihre E-Mail-Adresse eingeben.
        </Message>

        <div class="mb-4">
          <FloatLabel variant="on">
            <InputText id="errorEmail" v-model="currentEmail" type="email" class="w-full" />
            <label for="errorEmail">E-Mail-Adresse</label>
          </FloatLabel>
        </div>

        <Message v-if="successMessage" severity="success" class="mb-4 text-left">
          {{ successMessage }}
        </Message>

        <Button
          label="Neuen Link anfordern"
          icon="pi pi-send"
          class="w-full mb-4"
          :loading="resendLoading"
          :disabled="!currentEmail || cooldown > 0"
          @click="resendVerification"
        />
        <p v-if="cooldown > 0" class="text-sm text-gray-500 mb-4">
          Erneut senden möglich in {{ cooldown }} Sekunden
        </p>

        <RouterLink :to="{ name: 'anmelden' }" class="text-sm text-blue-600 hover:underline">
          Zurück zur Anmeldung
        </RouterLink>
      </div>

      <!-- verifying spinner -->
      <div v-else class="text-center">
        <div class="flex justify-center mb-6">
          <div class="w-20 h-20 rounded-full bg-gray-100 flex items-center justify-center">
            <i class="pi pi-spin pi-spinner text-gray-400" style="font-size: 2.25rem" />
          </div>
        </div>
        <h2 class="text-2xl font-bold text-gray-800 mb-3">Account wird bestätigt…</h2>
        <p class="text-gray-500">Bitte warten Sie einen Moment.</p>
      </div>

    </div>
  </div>

  <!-- email edit dialog -->
  <Dialog
    :visible="emailDialogVisible"
    @update:visible="emailDialogVisible = $event"
    header="E-Mail-Adresse korrigieren"
    :modal="true"
    :style="{ width: '24rem' }"
  >
    <p class="text-sm text-gray-600 mb-4">
      Geben Sie Ihre korrekte E-Mail-Adresse ein. Nach dem Speichern wird automatisch eine neue Bestätigungs-E-Mail versendet.
    </p>
    <FloatLabel variant="on">
      <InputText id="newEmail" v-model="newEmail" type="email" class="w-full" autofocus />
      <label for="newEmail">Neue E-Mail-Adresse</label>
    </FloatLabel>
    <small v-if="emailError" class="text-red-600 text-sm block mt-1">{{ emailError }}</small>
    <template #footer>
      <Button label="Abbrechen" text @click="emailDialogVisible = false" />
      <Button
        label="Speichern & erneut senden"
        icon="pi pi-check"
        :loading="emailLoading"
        :disabled="!newEmail || newEmail === currentEmail"
        @click="updateEmail"
      />
    </template>
  </Dialog>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { apiClient } from '@/services/axios'
import { useAuthStore } from '@/stores/auth'
import Button from 'openvue/button'
import InputText from 'openvue/inputtext'
import FloatLabel from 'openvue/floatlabel'
import Message from 'openvue/message'
import Dialog from 'openvue/dialog'

const route = useRoute()
const router = useRouter()
const authStore = useAuthStore()

// Email comes from the query param (set by both registration forms)
// or fall back to the auth store if the user is logged in
const currentEmail = ref(route.query.email || authStore.userEmail || '')

const verifyError = ref(false)
const resendLoading = ref(false)
const successMessage = ref('')
const cooldown = ref(0)
let cooldownTimer = null

const emailDialogVisible = ref(false)
const newEmail = ref('')
const emailLoading = ref(false)
const emailError = ref('')

onMounted(async () => {
  const token = route.query.token || null
  if (!token) return
  try {
    const response = await apiClient.post('/auth/verify', { token })
    if (response?.status === 200) {
      router.replace({ name: 'account-bestaetigen', query: { verify: 'success' } })
    } else {
      verifyError.value = true
    }
  } catch {
    verifyError.value = true
  }
})

async function resendVerification() {
  if (!currentEmail.value) return
  resendLoading.value = true
  successMessage.value = ''
  try {
    await apiClient.post('/auth/request-verify-token', { email: currentEmail.value })
    successMessage.value = 'Bestätigungs-E-Mail wurde gesendet. Bitte prüfen Sie Ihren Posteingang.'
    cooldown.value = 60
    cooldownTimer = setInterval(() => {
      cooldown.value -= 1
      if (cooldown.value <= 0) clearInterval(cooldownTimer)
    }, 1000)
  } finally {
    resendLoading.value = false
  }
}

function openEmailDialog() {
  newEmail.value = ''
  emailError.value = ''
  emailDialogVisible.value = true
}

async function updateEmail() {
  emailError.value = ''
  emailLoading.value = true
  try {
    await apiClient.patch('/users/me', { email: newEmail.value })
    currentEmail.value = newEmail.value
    authStore.userEmail = newEmail.value
    emailDialogVisible.value = false
    await resendVerification()
  } catch {
    emailError.value = 'E-Mail-Adresse konnte nicht gespeichert werden.'
  } finally {
    emailLoading.value = false
  }
}

onUnmounted(() => {
  if (cooldownTimer) clearInterval(cooldownTimer)
})
</script>
