<template>
  <li>
    <Dialog v-model:visible="dialogOffen" modal dismissableMask class="w-full max-w-6xl">
      <template #header>
        <div class="flex min-w-0 flex-1 flex-wrap items-start justify-between gap-3 pr-2">
          <div class="min-w-0 flex-1 basis-80">
            <p class="m-0 text-sm font-medium text-gray-500">
              Mobilitätscheck {{ nurAnsicht ? 'ansehen' : 'bearbeiten' }}
            </p>
            <h2
              class="m-0 text-xl font-extrabold leading-snug tracking-tight text-blue break-words hyphens-auto"
              lang="de"
            >
              {{ localItem?.name || props.item.name || 'Kein Name' }}
            </h2>
          </div>
        </div>
      </template>
      <div v-if="isLoadingItem" class="flex flex-col gap-4 p-2">
        <Skeleton height="3rem" />
        <div v-for="i in 4" :key="i" class="flex flex-col gap-3 p-4 border rounded-lg">
          <div class="flex items-center gap-3">
            <Skeleton shape="square" size="1.25rem" />
            <Skeleton width="14rem" height="1.25rem" />
          </div>
        </div>
      </div>
      <!-- key: beim Wechsel Ansicht → Bearbeiten neu aufbauen (Optionen werden nur im Bearbeitungsmodus geladen) -->
      <MobilitaetscheckFormularEingabeZielOber
        v-else-if="localItem"
        :key="nurAnsicht ? 'ansicht' : 'bearbeiten'"
        :editMode="dialogOffen"
        :readOnly="nurAnsicht"
        :item="localItem"
        @close-modal="dialogOffen = false"
        @reload-item="emit('reload-item', props.item.id)"
      />
    </Dialog>

    <div
      class="group flex flex-col gap-2 px-5 py-4 transition-colors hover:bg-gray-50 cursor-pointer"
      @click="oeffne(true)"
    >
      <!-- Name über die volle Breite, darunter Metadaten links und Aktionen rechts -->
      <button
        type="button"
        class="block max-w-full text-left text-base font-semibold leading-snug text-gray-900 break-words hyphens-auto group-hover:text-blue focus-visible:underline"
        lang="de"
        @click.stop="oeffne(true)"
      >
        {{ props.item.name || 'Kein Name' }}
      </button>

      <div class="flex flex-wrap items-center justify-between gap-x-4 gap-y-2">
        <p class="m-0 flex flex-wrap items-center gap-x-2 text-sm text-gray-500">
          <span class="flex items-center gap-1">
            <i class="pi pi-user text-xs" />
            {{ props.item.autor?.vorname }} {{ props.item.autor?.nachname }}
          </span>
          <template v-if="props.item.autor?.gruppe?.name">
            <span aria-hidden="true">·</span>
            <span>{{ props.item.autor.gruppe.name }}</span>
          </template>
          <span aria-hidden="true">·</span>
          <span class="flex items-center gap-1">
            <i class="pi pi-calendar text-xs" />
            {{ new Date(props.item.erstelltAm).toLocaleDateString('de-DE') }}
          </span>
        </p>

        <!-- Aktionen: Klicks hier sollen die Ansicht nicht öffnen -->
        <div class="ml-auto flex flex-wrap items-center gap-2" @click.stop>
          <ToggleButton
            v-if="!props.readOnly"
            v-model="veroeffentlicht"
            v-tooltip.top="
              veroeffentlicht
                ? 'Für andere sichtbar – klicken, um privat zu stellen'
                : 'Nur für Sie sichtbar – klicken, um zu veröffentlichen'
            "
            onLabel="öffentlich"
            offLabel="privat"
            onIcon="pi pi-lock-open"
            offIcon="pi pi-lock"
            size="small"
            style="width: 7.5rem"
            @change="onPublish"
          />

          <Button
            v-if="!props.readOnly"
            icon="pi pi-pen-to-square"
            label="bearbeiten"
            size="small"
            outlined
            @click="oeffne(false)"
          />

          <div class="flex items-center">
            <Button
              v-tooltip.top="
                exportDisabled
                  ? 'PDF-Export erst möglich, wenn zu jedem tangierten Ziel ein Unterziel ausgewählt ist'
                  : 'PDF exportieren'
              "
              icon="pi pi-file-pdf"
              severity="secondary"
              text
              rounded
              size="small"
              aria-label="PDF exportieren"
              :disabled="exportDisabled"
              @click="onExport"
            />
            <Button
              v-tooltip.top="'Duplizieren'"
              icon="pi pi-copy"
              severity="secondary"
              text
              rounded
              size="small"
              aria-label="Duplizieren"
              @click="onCopy"
            />
            <Button
              v-if="!props.readOnly"
              v-tooltip.top="'Löschen'"
              icon="pi pi-trash"
              severity="danger"
              text
              rounded
              size="small"
              aria-label="Löschen"
              @click="confirmDelete"
            />
          </div>
        </div>
      </div>
    </div>
  </li>
</template>

<script setup>
import Dialog from 'openvue/dialog'
import { ref, computed, onMounted } from 'vue'
import { fetchItems } from '@/composables/crud'

import ToggleButton from 'openvue/togglebutton'

import MobilitaetscheckFormularEingabeZielOber from '@/components/MobilitaetscheckFormularEingabeZielOber.vue'
import Button from 'openvue/button'

import Skeleton from 'openvue/skeleton'
import { useConfirm } from 'openvue/useconfirm'

const veroeffentlicht = ref()
const dialogOffen = ref(false)
const nurAnsicht = ref(true)
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

// Klick auf den Eintrag öffnet die Ansicht, „bearbeiten“ direkt das Formular.
const oeffne = async (ansicht) => {
  nurAnsicht.value = ansicht || props.readOnly
  dialogOffen.value = true
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
