<template>
  <div class="flex items-start justify-center pt-16 px-4">
    <div class="w-full max-w-md">
      <div class="text-center">
        <div class="flex justify-center mb-6">
          <div class="w-20 h-20 rounded-full bg-amber-100 flex items-center justify-center">
            <i class="pi pi-envelope text-amber-600" style="font-size: 2.25rem" />
          </div>
        </div>
        <h2 class="text-2xl font-bold text-gray-800 mb-3">E-Mail-Adresse bestätigen</h2>
        <p class="text-gray-600 mb-6">
          Ihr Account wurde noch nicht verifiziert. Bitte bestätigen Sie Ihre E-Mail-Adresse,
          um die Anwendung nutzen zu können.
        </p>

        <!-- assigned email display -->
        <div class="bg-gray-50 border border-gray-200 rounded-lg px-4 py-3 mb-6 text-left">
          <p class="text-xs text-gray-500 mb-0.5">Hinterlegte E-Mail-Adresse</p>
          <div class="flex items-center justify-between gap-2">
            <p class="text-sm font-medium text-gray-800 break-all">{{ authStore.userEmail }}</p>
            <Button
              v-if="isPolitik"
              icon="pi pi-pencil"
              text
              rounded
              size="small"
              aria-label="E-Mail-Adresse bearbeiten"
              @click="openDialog"
            />
          </div>
        </div>

        <div class="bg-amber-50 border border-amber-200 rounded-lg p-4 mb-6 text-left">
          <div class="flex gap-3">
            <i class="pi pi-info-circle text-amber-500 mt-0.5 shrink-0" />
            <p class="text-sm text-amber-800">
              Keine E-Mail erhalten? Bitte prüfen Sie auch Ihren Spam-Ordner oder fordern Sie
              eine neue Bestätigungs-E-Mail an.
            </p>
          </div>
        </div>

        <div v-if="successMessage" class="bg-green-50 border border-green-200 rounded-lg p-4 mb-6 text-left">
          <div class="flex gap-3">
            <i class="pi pi-check-circle text-green-500 mt-0.5 shrink-0" />
            <p class="text-sm text-green-800">{{ successMessage }}</p>
          </div>
        </div>

        <Button
          label="Bestätigungs-E-Mail erneut senden"
          icon="pi pi-send"
          class="w-full mb-4"
          :loading="resendLoading"
          :disabled="cooldown > 0"
          @click="resendVerification"
        />
        <p v-if="cooldown > 0" class="text-sm text-gray-500 mb-4">
          Erneut senden möglich in {{ cooldown }} Sekunden
        </p>

        <Button
          label="Bereits bestätigt? Erneut prüfen"
          icon="pi pi-refresh"
          text
          class="w-full mb-4"
          :loading="checkLoading"
          @click="checkVerified"
        />

        <RouterLink :to="{ name: 'anmelden' }" class="text-sm text-blue-600 hover:underline">
          Zurück zur Anmeldung
        </RouterLink>
      </div>
    </div>
  </div>

  <!-- email edit dialog (Politik only) -->
  <Dialog
    v-model:visible="dialogVisible"
    header="E-Mail-Adresse korrigieren"
    :modal="true"
    :style="{ width: '24rem' }"
    @hide="resetDialog"
  >
    <form @submit.prevent="updateEmail">
      <p class="text-sm text-gray-600 mb-4">
        Geben Sie Ihre korrekte E-Mail-Adresse ein. Nach dem Speichern wird
        automatisch eine neue Bestätigungs-E-Mail versendet.
      </p>
      <div class="mb-2">
        <FloatLabel variant="on">
          <InputText
            id="newEmail"
            v-model="newEmail"
            type="email"
            :disabled="emailLoading"
            autofocus
            class="w-full"
          />
          <label for="newEmail">Neue E-Mail-Adresse</label>
        </FloatLabel>
        <small v-if="emailError" class="p-error block mt-1">{{ emailError }}</small>
      </div>
    </form>
    <template #footer>
      <Button label="Abbrechen" text @click="dialogVisible = false" />
      <Button
        label="Speichern"
        icon="pi pi-check"
        :loading="emailLoading"
        :disabled="!newEmail || newEmail === authStore.userEmail"
        @click="updateEmail"
      />
    </template>
  </Dialog>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'
import { apiClient } from '@/services/axios'
import { useAuthStore } from '@/stores/auth'
import Button from 'openvue/button'
import InputText from 'openvue/inputtext'
import Dialog from 'openvue/dialog'
import FloatLabel from 'openvue/floatlabel'

const authStore = useAuthStore()
const router = useRouter()
const checkLoading = ref(false)

async function checkVerified() {
  checkLoading.value = true
  try {
    await authStore.refreshVerified()
    if (authStore.isVerified) {
      if (authStore.userRolleId === 3) {
        router.replace({ name: 'admin-kommunen' })
      } else {
        router.replace({ name: 'magistratsvorlage-liste' })
      }
    }
  } finally {
    checkLoading.value = false
  }
}

onMounted(checkVerified)

const isPolitik = computed(() => authStore.userRolleId === 2)

const dialogVisible = ref(false)
const newEmail = ref('')
const emailLoading = ref(false)
const emailError = ref('')

const resendLoading = ref(false)
const successMessage = ref('')
const cooldown = ref(0)
let cooldownTimer = null

function openDialog() {
  newEmail.value = ''
  emailError.value = ''
  dialogVisible.value = true
}

function resetDialog() {
  newEmail.value = ''
  emailError.value = ''
}

async function updateEmail() {
  emailError.value = ''
  emailLoading.value = true
  try {
    await apiClient.patch('/users/me', { email: newEmail.value })
    authStore.userEmail = newEmail.value
    dialogVisible.value = false
    await resendVerification()
  } catch {
    emailError.value = 'E-Mail-Adresse konnte nicht gespeichert werden.'
  } finally {
    emailLoading.value = false
  }
}

async function resendVerification() {
  if (!authStore.userEmail) return
  resendLoading.value = true
  successMessage.value = ''
  try {
    await apiClient.post('/auth/request-verify-token', { email: authStore.userEmail })
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

onUnmounted(() => {
  if (cooldownTimer) clearInterval(cooldownTimer)
})
</script>
