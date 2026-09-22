<template>
  <div
    v-if="zeigeBanner"
    class="flex items-start gap-2 p-3 bg-blue-50 border border-blue-200 rounded text-sm text-blue-800"
  >
    <i class="pi pi-info-circle mt-0.5 shrink-0" />
    <span class="flex-1">
      Neu hier? In der
      <router-link
        :to="{ name: 'dokumentation', hash: '#grundbausteine' }"
        class="underline font-semibold"
      >
        Dokumentation und Hilfe
      </router-link>
      finden Sie eine Anleitung, wie Sie Ihren ersten Mobilitätscheck erstellen.
    </span>
    <button
      type="button"
      class="pi pi-times shrink-0 cursor-pointer text-blue-800 hover:text-blue-900"
      aria-label="Hinweis schließen"
      @click="dismiss"
    />
  </div>
</template>

<script setup>
import { ref, computed, watch } from 'vue'
import { apiClient } from '@/services/axios'
import { useAuthStore } from '@/stores/auth'

const authStore = useAuthStore()

const hatEigeneMobilitaetschecks = ref(true)
const isDismissed = ref(false)

const storageKey = computed(() =>
  authStore.userId ? `dokumentationHinweisDismissed:${authStore.userId}` : null
)

const zeigeBanner = computed(
  () => authStore.isLoggedIn && !hatEigeneMobilitaetschecks.value && !isDismissed.value
)

const checkMobilitaetschecks = async () => {
  if (!authStore.isLoggedIn) return
  if (storageKey.value && localStorage.getItem(storageKey.value) === 'true') {
    isDismissed.value = true
  } else {
    isDismissed.value = false
  }
  try {
    const res = await apiClient.get('/mobilitaetscheck/eingabe/hat-eigene')
    hatEigeneMobilitaetschecks.value = res.data.hatEigene
  } catch {
    hatEigeneMobilitaetschecks.value = true
  }
}

const dismiss = () => {
  isDismissed.value = true
  if (storageKey.value) {
    localStorage.setItem(storageKey.value, 'true')
  }
}

watch(() => authStore.isLoggedIn, checkMobilitaetschecks, { immediate: true })
</script>
