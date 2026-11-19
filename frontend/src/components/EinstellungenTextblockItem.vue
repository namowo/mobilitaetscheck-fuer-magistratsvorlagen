<template>
  <Dialog
    v-model:visible="editMode"
    header="Textbaustein bearbeiten"
    modal
    dismissableMask
    class="w-full max-w-[50rem]"
  >
    <EinstellungenTextblockFormular
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
    :aria-label="andereGemeinde ? undefined : `Textbaustein ${kurztext} bearbeiten`"
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
        <i class="pi pi-align-left" />
      </span>
      <div class="min-w-0 flex-1">
        <div
          class="rich-content textblock-vorschau text-gray-900 break-words leading-snug line-clamp-4"
          v-html="props.item.name"
        />
        <div
          v-if="props.item.tags?.length"
          class="flex flex-wrap items-center gap-1.5 mt-2"
        >
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
import BadgeSichtbarkeit from '@/components/BadgeSichtbarkeit.vue'
import EinstellungenTextblockFormular from '@/components/EinstellungenTextblockFormular.vue'
import { htmlZuText } from '@/utils/html'

const props = defineProps({
  item: Object,
  tags: Array
})

const emit = defineEmits(['delete-item', 'update-item'])

const editMode = ref(false)

// Kurzer Klartext für Screenreader-Labels
const kurztext = computed(() => {
  const text = htmlZuText(props.item.name)
  return text.length > 60 ? `${text.slice(0, 60)}…` : text
})
const authStore = useAuthStore()

// Textbausteine anderer Kommunen sind sichtbar, aber nicht bearbeitbar
const andereGemeinde = computed(() => props.item.gemeindeId !== authStore.gemeindeId)

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

<style scoped>
.textblock-vorschau :deep(p:last-child),
.textblock-vorschau :deep(ul:last-child),
.textblock-vorschau :deep(ol:last-child) {
  margin-bottom: 0;
}
</style>
