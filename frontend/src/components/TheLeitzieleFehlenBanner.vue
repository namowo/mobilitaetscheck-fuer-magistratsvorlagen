<template>
  <div
    v-if="zeigeBanner"
    class="flex items-start gap-2 p-3 bg-amber-50 border border-amber-200 rounded text-sm text-amber-800"
  >
    <i class="pi pi-exclamation-triangle mt-0.5 shrink-0" />
    <template v-if="istLocalAdmin">
      <span>
        Für Ihre Kommune wurden noch keine Leitziele festgelegt.
        <router-link :to="{ name: 'leitziel-sets' }" class="underline font-semibold">
          Jetzt Leitziele einrichten
        </router-link>
      </span>
    </template>
    <template v-else>
      <span>Für Ihre Kommune wurden noch keine Leitziele festgelegt.</span>
    </template>
  </div>
</template>

<script setup>
import { ref, computed, watch } from 'vue'
import { apiClient } from '@/services/axios'
import { useAuthStore } from '@/stores/auth'

const authStore = useAuthStore()

const hatEigeneZielSets = ref(true)

const istLocalAdmin = computed(
  () => authStore.userRolleId === 1 || authStore.isLocalSuperuser
)

const istPlatformAdminOhneKommune = computed(
  () => authStore.userRolleId === 3 && !authStore.isLocalSuperuser
)

const zeigeBanner = computed(
  () => authStore.isLoggedIn && !istPlatformAdminOhneKommune.value && !hatEigeneZielSets.value
)

const checkZielSets = async () => {
  if (!authStore.isLoggedIn || istPlatformAdminOhneKommune.value) return
  try {
    const res = await apiClient.get('/einstellungen/mobilitaetscheck/ziel-set/hat-eigene')
    hatEigeneZielSets.value = res.data.hatEigene
  } catch {
    hatEigeneZielSets.value = true
  }
}

watch(() => authStore.isLoggedIn, checkZielSets, { immediate: true })
</script>
