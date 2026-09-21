<template>
  <div>
    <BaseModal v-model="editMode">
      <template #header>
        <h2>
          {{ localItem?.name || 'Kein Name' }} {{ props.readOnly ? 'anzeigen' : 'bearbeiten' }}
        </h2>
      </template>
      <div v-if="isLoadingItem" class="flex flex-col gap-4 p-2">
        <Skeleton height="3rem" />
        <div v-for="i in 4" :key="i" class="flex flex-col gap-3 p-4 border rounded-lg">
          <div class="flex items-center gap-3">
            <Skeleton shape="square" size="1.25rem" />
            <Skeleton width="14rem" height="1.25rem" />
          </div>
        </div>
        <div class="flex justify-end mt-2">
          <Skeleton width="8rem" height="2.5rem" />
        </div>
      </div>
      <MobilitaetscheckFormularEingabeZielOber
        v-else-if="localItem"
        :editMode="editMode"
        :readOnly="props.readOnly"
        :item="localItem"
        @close-modal="editMode = false"
        @reload-item="emit('reload-item', props.item.id)"
      />
    </BaseModal>
    <BaseCard>
      <div class="col-span-10 grid grid-cols-1 gap-x-4 gap-y-1">
        <h3 class="font-bold text-lg">{{ props.item.name || 'Kein Name' }}</h3>
        <div class="grid grid-cols-2 gap-4">
          <div class="flex items-center gap-2">
            <span class="font-semibold">Erstellt von</span>
            <span>
              {{ props.item.autor?.vorname }} {{ props.item.autor?.nachname }}
              <span v-if="props.item.autor?.gruppe?.name" class="text-gray-500">
                ({{ props.item.autor.gruppe.name }})
              </span>
            </span>
          </div>
          <div class="flex items-center gap-2">
            <span class="font-semibold">Erstellt am</span>
            <span>{{ new Date(props.item.erstelltAm).toLocaleDateString('de-DE') }}</span>
          </div>
        </div>
      </div>
      <div class="col-span-2 grid grid-cols-1 items-center gap-y-1">
        <div class="grid grid-cols-5 items-center gap-1">
          <div class="col-span-4 flex gap-2">
            <ToggleButton
              v-if="!props.readOnly"
              v-model="veroeffentlicht"
              onLabel="öffentlich"
              offLabel="privat"
              onIcon="pi pi-lock-open"
              offIcon="pi pi-lock"
              @change="onPublish"
              size="small"
              style="width: 8rem"
            />
            <Button
              :icon="props.readOnly ? 'pi pi-eye' : 'pi pi-pen-to-square'"
              @click="openEditModal"
              :label="props.readOnly ? 'Anzeigen' : 'bearbeiten'"
              size="small"
            />
            <Button
              icon="pi pi-download"
              @click="onExport"
              label="PDF-Export"
              size="small"
              :disabled="exportDisabled"
            />
            <Button icon="pi pi-copy" @click="onCopy" label="Duplizieren" size="small" />
          </div>
          <div class="flex justify-end">
            <Button
              v-if="!props.readOnly"
              icon="pi pi-trash"
              severity="danger"
              size="small"
              text
              @click="confirmDelete"
            />
          </div>
        </div>
      </div>
    </BaseCard>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { fetchItems } from '@/composables/crud'

import ToggleButton from 'openvue/togglebutton'

import MobilitaetscheckFormularEingabeZielOber from '@/components/MobilitaetscheckFormularEingabeZielOber.vue'
import Button from 'openvue/button'

import Skeleton from 'openvue/skeleton'
import { useConfirm } from 'openvue/useconfirm'

const veroeffentlicht = ref()
const editMode = ref(false)
const localItem = ref(null)
const isLoadingItem = ref(false)
const props = defineProps({
  item: Object,
  readOnly: {
    type: Boolean,
    default: false
  }
})

onMounted(() => {
  veroeffentlicht.value = props.item.veroeffentlicht
})

const openEditModal = async () => {
  editMode.value = true
  isLoadingItem.value = true
  localItem.value = await fetchItems(`mobilitaetscheck/eingabe/${props.item.id}`)
  isLoadingItem.value = false
}

const emit = defineEmits([
  'update-item',
  'delete-item',
  'publish-item',
  'export-item',
  'reload-item',
  'copy-item'
])

const onPublish = () => {
  emit('publish-item', {
    modelId: props.item.id,
    values: { veroeffentlicht: veroeffentlicht.value }
  })
}

const onExport = () => {
  emit('export-item', props.item.id)
}

const confirm = useConfirm()
const confirmDelete = () => {
  confirm.require({
    message: 'Möchten Sie diesen Mobilitätscheck löschen?',
    header: 'Löschen bestätigen',
    icon: 'pi pi-exclamation-triangle',
    rejectProps: { label: 'Abbrechen', severity: 'secondary', outlined: true },
    acceptProps: { label: 'Löschen', severity: 'danger' },
    accept: () => emit('delete-item', props.item.id)
  })
}

const onCopy = () => {
  emit('copy-item', props.item.id)
}

const exportDisabled = computed(() =>
  (props.item.eingabeZielOber ?? []).some(
    (ober) => ober.tangiert && !(ober.eingabeZielUnter ?? []).some((unter) => unter.tangiert)
  )
)
</script>

<style></style>
