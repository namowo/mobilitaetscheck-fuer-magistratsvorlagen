<template>
  <Dialog
    v-model:visible="editMode"
    header="Indikator bearbeiten"
    modal
    dismissableMask
    class="w-full max-w-[50rem]"
  >
    <EinstellungenIndikatorFormular
      :editMode="true"
      :item="props.item"
      :tags="props.tags"
      @update-item="onUpdate"
      @delete-item="onDelete"
    />
  </Dialog>
  <div
    :role="andereGemeinde ? undefined : 'button'"
    :tabindex="andereGemeinde ? undefined : 0"
    :aria-label="andereGemeinde ? undefined : `Indikator ${props.item.name} bearbeiten`"
    :class="[
      'group flex flex-col sm:flex-row sm:items-center gap-3 px-4 py-4 transition',
      andereGemeinde
        ? 'bg-gray-50'
        : 'cursor-pointer hover:bg-blue-100/40 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-inset focus-visible:ring-blue-400'
    ]"
    @click="openEdit"
    @keydown.enter.self="openEdit"
  >
    <div class="flex items-start gap-3 min-w-0 flex-1">
      <span
        class="flex h-9 w-9 shrink-0 items-center justify-center rounded-lg bg-blue-100 text-blue-700"
      >
        <i class="pi pi-chart-bar" />
      </span>
      <div class="min-w-0 flex-1">
        <p class="text-gray-900 break-words leading-snug">{{ props.item.name }}</p>
        <a
          v-if="props.item.quelleUrl"
          v-tooltip.top="'Quelle in neuem Tab öffnen'"
          :href="props.item.quelleUrl"
          target="_blank"
          rel="noopener noreferrer"
          class="mt-1 inline-flex max-w-full items-center gap-1 text-sm text-blue-700 hover:underline"
          @click.stop
          @keydown.stop
        >
          <i class="pi pi-external-link text-xs" />
          <span class="truncate">{{ quelleHost }}</span>
        </a>
        <div v-if="props.item.tags?.length" class="flex flex-wrap items-center gap-1.5 mt-2">
          <Tag
            v-for="tag in props.item.tags"
            :key="tag.id"
            :value="tag.name"
            severity="secondary"
            icon="pi pi-tag"
            class="!text-xs"
          />
        </div>
      </div>
    </div>
    <div class="pl-12 sm:pl-0 shrink-0">
      <BadgeSichtbarkeit
        :gemeindespezifisch="props.item.gemeindespezifisch"
        :andereGemeinde="andereGemeinde"
      />
    </div>
  </div>
</template>

<script setup>
import Dialog from 'openvue/dialog'
import { computed, ref } from 'vue'
import { useAuthStore } from '@/stores/auth'
import Tag from 'openvue/tag'
import EinstellungenIndikatorFormular from '@/components/EinstellungenIndikatorFormular.vue'
import BadgeSichtbarkeit from '@/components/BadgeSichtbarkeit.vue'

const props = defineProps({
  item: Object,
  tags: Array
})

const emit = defineEmits(['delete-item', 'update-item'])

const editMode = ref(false)
const authStore = useAuthStore()

// Indikatoren anderer Kommunen sind sichtbar, aber nicht bearbeitbar
const andereGemeinde = computed(() => props.item.gemeindeId !== authStore.gemeindeId)

// Kompakte Anzeige der Quelle (nur Domain)
const quelleHost = computed(() => {
  try {
    return new URL(props.item.quelleUrl).hostname.replace(/^www\./, '')
  } catch {
    return props.item.quelleUrl
  }
})

const openEdit = () => {
  if (andereGemeinde.value) return
  editMode.value = true
}

const onUpdate = (values) => {
  emit('update-item', values)
  editMode.value = false
}

const onDelete = (modelId) => {
  emit('delete-item', modelId)
  editMode.value = false
}
</script>
