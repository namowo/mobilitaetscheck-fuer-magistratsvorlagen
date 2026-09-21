<template>
  <div>
    <DataView
      :value="isLoading ? Array(5).fill({}) : klimarelevanzpruefungListe"
      paginator
      :rows="10"
    >
      <template #list="slotProps">
        <div class="flex flex-col">
          <template v-if="isLoading === true">
            <div v-for="i in slotProps.items" :key="i">
              <BaseCard>
                <div class="flex flex-col xl:flex-row xl:items-start gap-6">
                  <Skeleton class="!w-9/12 sm:!w-64 xl:!w-40 !h-24 mx-auto" />
                  <div
                    class="flex flex-col sm:flex-row justify-between items-center xl:items-start flex-1 gap-6"
                  >
                    <div class="flex flex-col items-center sm:items-start gap-4">
                      <Skeleton width="8rem" height="2rem" />
                      <Skeleton width="6rem" height="1rem" />
                    </div>
                    <div class="flex sm:flex-col items-center sm:items-end gap-4 sm:gap-2">
                      <Skeleton width="4rem" height="2rem" />
                      <Skeleton size="3rem" shape="circle" />
                    </div>
                  </div>
                </div>
              </BaseCard>
            </div>
          </template>
          <template v-else>
            <div v-for="(item, index) in slotProps.items" :key="index">
              <router-link
                :to="{
                  name: 'magistratsvorlage-id-klimarelevanzpruefung-id',
                  params: { klimarelevanzpruefungId: item.id }
                }"
                custom
                v-slot="{ navigate, href }"
              >
                <BaseCard class="hover:bg-gray-50" :data-href="href" tabindex="0">
                  <template #header>
                    <span class="font-bold text-lg">{{ item.name }}{{ item.Id }}</span>
                  </template>
                  <div class="grid grid-cols-12 gap-4">
                    <div class="col-span-5 flex grid grid-cols-5 gap-x-2">
                      <div class="col-span-2 font-bold grid grid-cols-1 gap-y-1">
                        <div>Erstellt am</div>
                      </div>
                      <div class="col-span-3 grid grid-cols-1">
                        <div>{{ datumFormatieren(item.erstelltAm) }}</div>
                      </div>
                    </div>
                    <div class="col-span-4 font-bold flex items-center justify-end">
                      <div class="flex items-center gap-2">
                        <Tag value="A" :severity="getTagSeverity(item.f1, item.fb1)" />
                        <Tag value="B" :severity="getTagSeverity(item.f2, item.fb2)" />
                        <Tag value="C" :severity="getTagSeverity(item.f3, item.fb3)" />
                        <Tag value="D" :severity="getTagSeverity(item.f4, item.fb4)" />
                        <Tag value="E" :severity="item.f5 ? 'success' : 'secondary'" />
                      </div>
                    </div>
                  </div>
                  <div class="grid grid-cols-12">
                    <div class="col-span-7 grid grid-cols-1 justify-start gap-2">
                      <div class="flex gap-2">
                        <Button
                          icon="pi pi-pen-to-square"
                          @click="navigate"
                          label="bearbeiten"
                          size="small"
                        />
                        <Button
                          icon="pi pi-download"
                          @click="onExport(item.id)"
                          label="PDF-Export"
                          size="small"
                          :disabled="!canExport(item)"
                          v-tooltip="!canExport(item) ? 'Bitte alle Fragebögen vollständig ausfüllen' : undefined"
                        />
                      </div>
                    </div>
                    <div class="col-span-5 grid grid-cols-1">
                      <div class="flex justify-end">
                        <ButtonLoeschen @delete-confirmed="() => onDelete(item.id)" />
                      </div>
                    </div>
                  </div>
                </BaseCard>
              </router-link>
            </div>
          </template>
        </div>
      </template>
    </DataView>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { deleteItem, exportItem, fetchItems } from '@/composables/crud'
import Button from 'openvue/button'
import ButtonLoeschen from '@/components/ButtonLoeschen.vue'
import DataView from 'openvue/dataview'
import Tag from 'openvue/tag'
import Skeleton from 'openvue/skeleton'
import BaseCard from '@/components/BaseCard.vue'

const klimarelevanzpruefungListe = ref([])
const isLoading = ref(true)

const route = useRoute()

onMounted(async () => {
  isLoading.value = true
  await fetchData()
  isLoading.value = false
})

const fetchData = async () => {
  klimarelevanzpruefungListe.value = await fetchItems(
    `klimarelevanzpruefung/eingabe/magistratsvorlage/${route.params.id}`
  )
}

const datumFormatieren = (datum) => {
  if (!datum) return '-'
  return new Date(datum).toLocaleDateString('de-DE', {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit'
  })
}

const getTagSeverity = (fEnabled, fb) => {
  if (!fEnabled) return 'secondary'
  if (fb?.fertig) return 'success'
  if (fb) return 'warn'
  return 'info'
}

const canExport = (item) => {
  const checks = [
    { f: item.f1, fb: item.fb1 },
    { f: item.f2, fb: item.fb2 },
    { f: item.f3, fb: item.fb3 },
    { f: item.f4, fb: item.fb4 }
  ]
  return checks.every(({ f, fb }) => !f || fb?.fertig === true)
}

const onExport = async (modelId) => {
  await exportItem({
    model: 'klimarelevanzpruefung',
    modelId,
    detail: {
      success: 'Klimarelevanzpruefung erfolgreich exportiert',
      error: 'Fehler beim Exportieren des Mobilitätschecks'
    }
  })
}

const onDelete = async (modelId) => {
  await deleteItem({
    model: 'klimarelevanzpruefung/eingabe',
    modelId,
    detail: {
      success: 'Klimacheck erfolgreich gelöscht',
      error: 'Fehler beim Löschen des Klimacheck'
    }
  })
  const index = klimarelevanzpruefungListe.value.findIndex((eingabe) => eingabe.id === modelId)
  klimarelevanzpruefungListe.value.splice(index, 1)
}
</script>

<style></style>
