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
      <span>
        Für Ihre Kommune wurden noch keine Leitziele festgelegt. Die Verwaltung muss diese hinterlegen.
      </span>
    </template>
  </div>
</template>

<script setup>
import { computed, watch } from 'vue'
import { useLeitzieleStatus } from '@/composables/leitzieleStatus'
import { useAuthStore } from '@/stores/auth'
import { useRoute } from 'vue-router'

const authStore = useAuthStore()
const route = useRoute()

const { hatEigeneZielSets, pruefe } = useLeitzieleStatus()

const istLocalAdmin = computed(
  () => authStore.effectiveRolleId === 1 || authStore.effectiveIsLocalSuperuser
)

const istPlatformAdminOhneKommune = computed(
  () => authStore.canSwitchView && authStore.effectiveRolleId === 3
)

const zeigeBanner = computed(
  () => authStore.isLoggedIn && !istPlatformAdminOhneKommune.value && !hatEigeneZielSets.value
)

const checkZielSets = async () => {
  if (!authStore.isLoggedIn || istPlatformAdminOhneKommune.value) return
  await pruefe()
}

// Re-check on navigation so the notice disappears as soon as the Kommune has set Leitziele
watch(() => [authStore.isLoggedIn, authStore.effectiveRolleId, route.fullPath], checkZielSets, {
  immediate: true
})
</script>
