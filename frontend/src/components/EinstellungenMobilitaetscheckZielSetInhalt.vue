<template>
  <div class="p-3">
    <BaseSpinner v-if="isLoading" class="my-2" />

    <div v-else-if="!setDetail" class="text-gray-400 text-sm">Keine Daten verfügbar.</div>

    <div v-else>
      <draggable
        v-model="editableOber"
        handle=".drag-handle-ober"
        item-key="id"
        :disabled="!editable"
        @end="onReorderOber"
      >
        <template #item="{ element: ober }">
          <div class="mb-3 border border-gray-200 rounded">
            <!-- Oberziel header -->
            <div class="flex items-center gap-2 px-3 py-2 bg-gray-50 rounded-t">
              <span v-if="editable" class="drag-handle-ober cursor-grab text-gray-400 select-none">⠿</span>
              <span class="text-sm font-semibold text-gray-500 w-6 shrink-0">{{ ober.nr }}.</span>

              <template v-if="ober._editing">
                <input
                  v-model="ober._editName"
                  class="flex-1 border border-gray-300 rounded px-2 py-0.5 text-sm"
                  @keyup.enter="saveOber(ober)"
                  @keyup.escape="cancelOber(ober)"
                  v-focus
                />
              </template>
              <span v-else class="flex-1 text-sm font-semibold">{{ ober.name }}</span>

              <template v-if="editable && !ober._editing">
                <Button
                  icon="pi pi-pencil"
                  size="small"
                  severity="secondary"
                  text
                  rounded
                  @click.stop="startEditOber(ober)"
                />
                <Button
                  icon="pi pi-trash"
                  size="small"
                  severity="danger"
                  text
                  rounded
                  @click.stop="deleteOber(ober)"
                />
              </template>
              <template v-if="editable && ober._editing">
                <Button icon="pi pi-check" size="small" severity="success" text rounded @click.stop="saveOber(ober)" />
                <Button icon="pi pi-times" size="small" severity="secondary" text rounded @click.stop="cancelOber(ober)" />
              </template>
            </div>

            <!-- Unterziele -->
            <div class="px-3 pb-2">
              <draggable
                v-model="ober._unterList"
                handle=".drag-handle-unter"
                item-key="id"
                :disabled="!editable"
                @end="() => onReorderUnter(ober)"
              >
                <template #item="{ element: unter }">
                  <div class="flex items-center gap-2 py-1 ml-4">
                    <span v-if="editable" class="drag-handle-unter cursor-grab text-gray-300 select-none text-xs">⠿</span>
                    <span class="text-xs text-gray-500 w-8 shrink-0">{{ ober.nr }}.{{ unter.nr }}</span>

                    <template v-if="unter._editing">
                      <input
                        v-model="unter._editName"
                        class="flex-1 border border-gray-300 rounded px-2 py-0.5 text-xs"
                        @keyup.enter="saveUnter(unter, ober)"
                        @keyup.escape="cancelUnter(unter, ober)"
                        v-focus
                      />
                    </template>
                    <span v-else class="flex-1 text-sm text-gray-700">{{ unter.name }}</span>

                    <template v-if="editable && !unter._editing">
                      <Button icon="pi pi-pencil" size="small" severity="secondary" text rounded @click.stop="startEditUnter(unter)" />
                      <Button icon="pi pi-trash" size="small" severity="danger" text rounded @click.stop="deleteUnter(unter, ober)" />
                    </template>
                    <template v-if="editable && unter._editing">
                      <Button icon="pi pi-check" size="small" severity="success" text rounded @click.stop="saveUnter(unter, ober)" />
                      <Button icon="pi pi-times" size="small" severity="secondary" text rounded @click.stop="cancelUnter(unter, ober)" />
                    </template>
                  </div>
                </template>
              </draggable>

              <div v-if="editable" class="ml-4 mt-1">
                <Button
                  label="Unterziel hinzufügen"
                  icon="pi pi-plus"
                  size="small"
                  severity="secondary"
                  text
                  @click="addUnter(ober)"
                />
              </div>
            </div>
          </div>
        </template>
      </draggable>

      <div v-if="editableOber.length === 0 && editable" class="mb-3 p-3 bg-yellow-50 border border-yellow-300 rounded text-sm text-yellow-800">
        Noch keine Leitziele vorhanden. Füge mindestens ein Oberziel mit Unterzielen hinzu, damit dieses Set für Mobilitätschecks genutzt werden kann.
      </div>
      <div v-else-if="editableOber.length === 0" class="text-gray-400 text-sm">
        Keine Ziele in diesem Set.
      </div>

      <div v-if="editable" class="mt-2">
        <Button
          label="Oberziel hinzufügen"
          icon="pi pi-plus"
          size="small"
          @click="addOber"
        />
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import draggable from 'vuedraggable'
import { apiClient } from '@/services/axios'
import { toastService } from '@/services/toast'
import Button from 'openvue/button'
import BaseSpinner from '@/components/BaseSpinner.vue'

const props = defineProps({
  set: { type: Object, required: true },
  editable: { type: Boolean, default: false }
})

const emit = defineEmits(['loaded'])

const OBER_API = 'einstellungen/mobilitaetscheck/ziel-set-ober'
const UNTER_API = 'einstellungen/mobilitaetscheck/ziel-set-unter'
const SET_API = 'einstellungen/mobilitaetscheck/ziel-set'

const isLoading = ref(false)
const setDetail = ref(null)
const editableOber = ref([])

// v-focus directive: auto-focus an input when it appears
const vFocus = { mounted: (el) => el.focus() }

const toEditable = (ober) => ({
  ...ober,
  _editing: false,
  _editName: ober.name,
  _unterList: [...(ober.zieleUnter ?? [])].sort((a, b) => a.nr - b.nr).map((u) => ({
    ...u,
    _editing: false,
    _editName: u.name
  }))
})

const loadSet = async () => {
  isLoading.value = true
  try {
    const response = await apiClient.get(`/${SET_API}/${props.set.id}`)
    setDetail.value = response.data
    editableOber.value = [...(response.data.zieleOber ?? [])]
      .sort((a, b) => a.nr - b.nr)
      .map(toEditable)
    emit('loaded', { hasZiele: editableOber.value.length > 0 })
  } catch {
    // no access or not found – leave null
  } finally {
    isLoading.value = false
  }
}

onMounted(loadSet)

// --- Oberziel ---
const startEditOber = (ober) => {
  ober._editName = ober.name
  ober._editing = true
}

const cancelOber = (ober) => {
  if (ober._isNew) {
    editableOber.value = editableOber.value.filter((o) => o !== ober)
    renumberOber()
  } else {
    ober._editing = false
  }
}

const saveOber = async (ober) => {
  if (!ober._editing) return
  const trimmed = ober._editName?.trim()

  if (!trimmed) {
    // discard draft or cancel edit
    if (ober._isNew) {
      editableOber.value = editableOber.value.filter((o) => o !== ober)
      renumberOber()
    } else {
      ober._editing = false
    }
    return
  }

  if (trimmed === ober.name) {
    ober._editing = false
    return
  }

  try {
    if (ober._isNew) {
      const response = await apiClient.post(`/${OBER_API}`, { zielSetId: props.set.id, name: trimmed })
      const idx = editableOber.value.indexOf(ober)
      editableOber.value.splice(idx, 1, toEditable(response.data))
    } else {
      await apiClient.patch(`/${OBER_API}/${ober.id}`, { name: trimmed })
      ober.name = trimmed
      ober._editing = false
    }
  } catch {
    toastService.add({ severity: 'error', detail: 'Fehler beim Speichern des Oberziels' })
    ober._editing = false
  }
}

const deleteOber = async (ober) => {
  try {
    await apiClient.delete(`/${OBER_API}/${ober.id}`)
    editableOber.value = editableOber.value.filter((o) => o.id !== ober.id)
    renumberOber()
  } catch {
    toastService.add({ severity: 'error', detail: 'Fehler beim Löschen des Oberziels' })
  }
}

const addOber = () => {
  editableOber.value.push({
    id: null,
    nr: editableOber.value.length + 1,
    name: '',
    _editing: true,
    _editName: '',
    _isNew: true,
    _unterList: []
  })
}

const onReorderOber = async () => {
  const ids = editableOber.value.map((o) => o.id)
  try {
    await apiClient.post(`/${OBER_API}/reorder`, { zielSetId: props.set.id, ids })
    editableOber.value.forEach((o, i) => { o.nr = i + 1 })
  } catch {
    toastService.add({ severity: 'error', detail: 'Fehler beim Umsortieren' })
    await loadSet()
  }
}

const renumberOber = () => {
  editableOber.value.forEach((o, i) => { o.nr = i + 1 })
}

// --- Unterziel ---
const startEditUnter = (unter) => {
  unter._editName = unter.name
  unter._editing = true
}

const cancelUnter = (unter, ober) => {
  if (unter._isNew) {
    ober._unterList = ober._unterList.filter((u) => u !== unter)
  } else {
    unter._editing = false
  }
}

const saveUnter = async (unter, ober) => {
  if (!unter._editing) return
  const trimmed = unter._editName?.trim()

  if (!trimmed) {
    if (unter._isNew) {
      ober._unterList = ober._unterList.filter((u) => u !== unter)
    } else {
      unter._editing = false
    }
    return
  }

  if (trimmed === unter.name) {
    unter._editing = false
    return
  }

  try {
    if (unter._isNew) {
      const response = await apiClient.post(`/${UNTER_API}`, { zielSetOberId: ober.id, name: trimmed })
      const idx = ober._unterList.indexOf(unter)
      ober._unterList.splice(idx, 1, { ...response.data, _editing: false, _editName: response.data.name })
    } else {
      await apiClient.patch(`/${UNTER_API}/${unter.id}`, { name: trimmed })
      unter.name = trimmed
      unter._editing = false
    }
  } catch {
    toastService.add({ severity: 'error', detail: 'Fehler beim Speichern des Unterziels' })
    unter._editing = false
  }
}

const deleteUnter = async (unter, ober) => {
  try {
    await apiClient.delete(`/${UNTER_API}/${unter.id}`)
    ober._unterList = ober._unterList.filter((u) => u.id !== unter.id)
    ober._unterList.forEach((u, i) => { u.nr = i + 1 })
  } catch {
    toastService.add({ severity: 'error', detail: 'Fehler beim Löschen des Unterziels' })
  }
}

const addUnter = (ober) => {
  ober._unterList.push({
    id: null,
    nr: ober._unterList.length + 1,
    name: '',
    _editing: true,
    _editName: '',
    _isNew: true
  })
}

const onReorderUnter = async (ober) => {
  const ids = ober._unterList.map((u) => u.id)
  try {
    await apiClient.post(`/${UNTER_API}/reorder`, { zielSetOberId: ober.id, ids })
    ober._unterList.forEach((u, i) => { u.nr = i + 1 })
  } catch {
    toastService.add({ severity: 'error', detail: 'Fehler beim Umsortieren' })
    await loadSet()
  }
}
</script>

<style scoped></style>
