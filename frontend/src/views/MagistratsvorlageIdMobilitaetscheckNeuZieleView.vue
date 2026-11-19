<template>
  <div class="max-w-6xl">
    <div class="grid grid-cols-2 w-full items-center">
      <BaseSubheading>Neuer Mobilitätscheck</BaseSubheading>
      <div class="flex w-full justify-end">
        <ButtonZuruecksetzen :disabled="isLoading" @click="confirmReset()">zurücksetzen</ButtonZuruecksetzen>
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
import { fetchItem, updateItemSilent } from '@/composables/crud'
import { useConfirm } from 'openvue/useconfirm'
import { useToast } from 'openvue/usetoast'
import ButtonZuruecksetzen from '@/components/ButtonZuruecksetzen.vue'
import { useRoute } from 'vue-router'
import MobilitaetscheckFormularEingabeZielOber from '@/components/MobilitaetscheckFormularEingabeZielOber.vue'
import Skeleton from 'openvue/skeleton'

const route = useRoute()
const confirm = useConfirm()
const toast = useToast()

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

// Alle Eingaben werden automatisch gespeichert – ein Neuladen der Seite setzt daher nichts
// zurück. Stattdessen werden alle Ober- und Unterziele serverseitig auf leer gesetzt.
const resetEingaben = async () => {
  isLoading.value = true
  const oberziele = eingabeZielOber.value?.eingabeZielOber ?? []
  try {
    await Promise.all(
      oberziele.flatMap((ober) => [
        updateItemSilent({
          model: 'mobilitaetscheck/eingabe/ziel/ober',
          modelId: ober.id,
          values: { tangiert: false, eingabeId: ober.eingabeId, zielOberId: ober.zielOberId }
        }),
        ...(ober.eingabeZielUnter ?? []).map((unter) =>
          updateItemSilent({
            model: 'mobilitaetscheck/eingabe/ziel/unter',
            modelId: unter.id,
            values: {
              tangiert: false,
              auswirkung: 0,
              auswirkungRaeumlichId: null,
              anmerkung: null,
              indikatorIds: [],
              eingabeZielOberId: unter.eingabeZielOberId,
              zielUnterId: unter.zielUnterId
            }
          })
        )
      ])
    )
    toast.add({ severity: 'success', detail: 'Eingaben wurden zurückgesetzt.', life: 3000 })
  } finally {
    await fetchEingabeZielOber()
  }
}

const confirmReset = () => {
  confirm.require({
    message:
      'Alle Angaben zu Ober- und Unterzielen dieses Mobilitätschecks werden gelöscht. Der Name bleibt erhalten.',
    header: 'Eingaben zurücksetzen',
    icon: 'pi pi-exclamation-triangle',
    rejectProps: { label: 'Abbrechen', severity: 'secondary', outlined: true },
    acceptProps: { label: 'Zurücksetzen', severity: 'danger' },
    accept: resetEingaben
  })
}
</script>

<style></style>
