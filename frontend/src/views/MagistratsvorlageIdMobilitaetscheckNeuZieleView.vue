<template>
  <div class="max-w-6xl">
    <div class="grid grid-cols-2 w-full items-center">
      <BaseHeading>Neuer Mobilitätscheck</BaseHeading>
      <div class="flex w-full justify-end">
        <ButtonZuruecksetzen @click="refreshPage()">zurücksetzen</ButtonZuruecksetzen>
      </div>
    </div>
    <div v-if="isLoading" class="grid grid-cols-1 gap-y-4 mt-4">
      <Skeleton height="3.5rem" class="w-full rounded-lg" />
      <div
        v-for="i in 3"
        :key="i"
        class="p-4 bg-white border border-gray-200 rounded-lg shadow space-y-3"
      >
        <div class="flex items-center gap-3">
          <Skeleton shape="circle" size="1.25rem" />
          <Skeleton height="1.25rem" width="50%" />
        </div>
      </div>
      <div class="flex justify-end mt-2">
        <Skeleton height="2.5rem" width="8rem" class="rounded-lg" />
      </div>
    </div>
    <div v-else>
      <MobilitaetscheckFormularEingabeZielOber :item="eingabeZielOber" />
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { fetchItem } from '@/composables/crud'
import ButtonZuruecksetzen from '@/components/ButtonZuruecksetzen.vue'
import { useRoute, useRouter } from 'vue-router'
import MobilitaetscheckFormularEingabeZielOber from '@/components/MobilitaetscheckFormularEingabeZielOber.vue'
import Skeleton from 'openvue/skeleton'

const route = useRoute()
const router = useRouter()

const eingabeZielOber = ref({})
const isLoading = ref(false)

const fetchEingabeZielOber = async () => {
  isLoading.value = true
  const checkId = route.params.checkId
  if (checkId) {
    eingabeZielOber.value = await fetchItem(`/mobilitaetscheck/eingabe/${checkId}`)
  }
  isLoading.value = false
}

onMounted(async () => {
  await fetchEingabeZielOber()
})

const refreshPage = () => {
  router.go() // Reloads the current route
}
</script>

<style></style>
