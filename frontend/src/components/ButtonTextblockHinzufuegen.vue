<template>
  <div class="max-w-5xl">
    <div
      class="flex items-center gap-2 cursor-pointer select-none text-gray-600 hover:text-gray-900"
      @click="showList = !showList"
    >
      <i :class="showList ? 'pi pi-chevron-down' : 'pi pi-chevron-right'" class="text-xs" />
      <span class="text-sm font-medium">Textbausteine</span>
    </div>

    <transition name="slide">
      <div v-if="showList" class="mt-2 border border-gray-200 rounded-lg bg-white shadow-sm">
        <!-- Filter-Bereich -->
        <div class="p-3 border-b border-gray-100 flex flex-col gap-2">
          <InputText
            v-model="searchQuery"
            placeholder="Suchen..."
            class="w-full"
            size="small"
          />
          <div v-if="allTags.length > 0">
            <div ref="tagRowRef" :class="['flex gap-1', showAllTags ? 'flex-wrap' : 'overflow-hidden h-6']">
              <Tag
                v-for="tag in allTags"
                :key="tag.id"
                :value="tag.name"
                :severity="selectedTagIds.includes(tag.id) ? 'primary' : 'secondary'"
                class="cursor-pointer flex-none"
                @click="toggleTag(tag.id)"
              />
            </div>
            <button
              v-if="hasOverflow || showAllTags"
              class="mt-1 text-xs text-gray-400 hover:text-gray-600"
              @click.stop="showAllTags = !showAllTags"
            >
              {{ showAllTags ? 'Weniger anzeigen' : 'Alle Tags anzeigen' }}
            </button>
          </div>
        </div>

        <!-- Textbausteinliste -->
        <ul class="max-h-48 overflow-y-auto">
          <li
            v-if="filteredTextblocks.length === 0"
            class="px-3 py-2 text-sm text-gray-400 italic"
          >
            Keine Textbausteine gefunden
          </li>
          <li
            v-for="block in filteredTextblocks"
            :key="block.id"
            class="px-3 py-2 text-sm cursor-pointer hover:bg-gray-100 border-b border-gray-50 last:border-0"
            @click="addTextblock(block)"
          >
            {{ block.name }}
          </li>
        </ul>

        <!-- Fußzeile: neuen Textbaustein anlegen -->
        <div class="px-3 py-2 border-t border-gray-100">
          <button
            class="flex items-center gap-1 text-xs text-gray-500 hover:text-gray-800"
            @click.stop="isModalOpen = true"
          >
            <i class="pi pi-plus text-xs" />
            Neuer Textbaustein
          </button>
        </div>
      </div>
    </transition>

    <BaseModal v-model="isModalOpen" @close="isModalOpen = false">
      <template #header>
        <h2>Neuen Textbaustein anlegen</h2>
      </template>
      <EinstellungenTextblockFormular
        :editMode="false"
        :tags="availableTags"
        @add-item="onCreateTextblock"
      />
    </BaseModal>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch, nextTick } from 'vue'
import Tag from 'openvue/tag'
import InputText from 'openvue/inputtext'
import { fetchItems, createItem } from '@/composables/crud'
import BaseModal from '@/components/BaseModal.vue'
import EinstellungenTextblockFormular from '@/components/EinstellungenTextblockFormular.vue'

const textblocks = ref([])
const availableTags = ref([])
const showList = ref(false)
const selectedTagIds = ref([])
const searchQuery = ref('')
const showAllTags = ref(false)
const hasOverflow = ref(false)
const tagRowRef = ref(null)
const isModalOpen = ref(false)

onMounted(async () => {
  ;[textblocks.value, availableTags.value] = await Promise.all([
    fetchItems('/einstellungen/textblock'),
    fetchItems('/einstellungen/tag')
  ])
})

watch(showList, async (val) => {
  if (val) {
    await nextTick()
    checkOverflow()
  }
})

const checkOverflow = () => {
  if (tagRowRef.value) {
    hasOverflow.value = tagRowRef.value.scrollWidth > tagRowRef.value.clientWidth
  }
}

const emit = defineEmits(['textblock-hinzufuegen'])

const allTags = computed(() => {
  const tagMap = new Map()
  for (const block of textblocks.value) {
    for (const tag of block.tags ?? []) {
      if (!tagMap.has(tag.id)) tagMap.set(tag.id, tag)
    }
  }
  return [...tagMap.values()].sort((a, b) => a.name.localeCompare(b.name))
})

const toggleTag = (tagId) => {
  const idx = selectedTagIds.value.indexOf(tagId)
  if (idx === -1) {
    selectedTagIds.value.push(tagId)
  } else {
    selectedTagIds.value.splice(idx, 1)
  }
}

const filteredTextblocks = computed(() => {
  let result = textblocks.value
  if (selectedTagIds.value.length > 0) {
    result = result.filter((block) =>
      block.tags?.some((tag) => selectedTagIds.value.includes(tag.id))
    )
  }
  if (searchQuery.value.trim()) {
    const q = searchQuery.value.toLowerCase()
    result = result.filter((block) => block.name.toLowerCase().includes(q))
  }
  return result
})

const addTextblock = (block) => {
  emit('textblock-hinzufuegen', block.name)
}

const onCreateTextblock = async (values) => {
  const newBlock = await createItem({
    model: 'einstellungen/textblock',
    values,
    detail: {
      success: 'Textbaustein erfolgreich angelegt',
      error: 'Fehler beim Anlegen des Textbausteins'
    }
  })
  textblocks.value.unshift(newBlock)
  isModalOpen.value = false
}
</script>

<style scoped>
.slide-enter-active,
.slide-leave-active {
  @apply transition-all duration-200;
}

.slide-enter-from,
.slide-leave-to {
  @apply opacity-0 -translate-y-1;
}
</style>
