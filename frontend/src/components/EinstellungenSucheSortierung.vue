<template>
  <!-- Toolbar für Einstellungslisten: Suche + Filter-Drawer (wie bei den Magistratsvorlagen) -->
  <div>
    <Drawer v-model:visible="drawerVisible" header="Filter" position="right">
      <div class="grid grid-cols-1 gap-6">
        <div>
          <label for="sortierung" class="mb-2 block font-bold">Sortieren nach</label>
          <Select
            inputId="sortierung"
            v-model="sortierung"
            :options="optionen"
            optionLabel="label"
            optionValue="value"
            class="w-full"
          />
        </div>

        <div v-if="mitSichtbarkeit">
          <label class="mb-2 block font-bold">Sichtbarkeit</label>
          <Listbox
            v-model="sichtbarkeit"
            :options="sichtbarkeitOptionen"
            optionLabel="label"
            optionValue="value"
            :allowEmpty="false"
            class="w-full"
          />
        </div>

        <div v-if="tagOptionen">
          <label class="mb-2 block font-bold">Tags</label>
          <Listbox
            v-model="tagIds"
            :options="tagOptionen"
            optionLabel="name"
            optionValue="id"
            multiple
            filter
            filterPlaceholder="Tag suchen"
            listStyle="max-height: 14rem"
            class="w-full"
            emptyMessage="Keine Tags vorhanden"
          />
        </div>

        <div v-if="zusatzOptionen.length" class="grid grid-cols-1 gap-3">
          <div
            v-for="option in zusatzOptionen"
            :key="option.key"
            class="flex items-center justify-between gap-3"
          >
            <label :for="`zusatz-${option.key}`">{{ option.label }}</label>
            <ToggleSwitch :inputId="`zusatz-${option.key}`" v-model="zusatz[option.key]" />
          </div>
        </div>

        <Button
          icon="pi pi-undo"
          label="Filter zurücksetzen"
          severity="secondary"
          outlined
          @click="emit('zuruecksetzen')"
        />
      </div>
    </Drawer>

    <div class="flex flex-col sm:flex-row sm:items-center gap-3">
      <IconField class="w-full sm:max-w-md">
        <InputIcon class="pi pi-search" />
        <InputText
          v-model="suche"
          :placeholder="suchLabel"
          :aria-label="suchLabel"
          class="w-full"
        />
      </IconField>
      <span
        v-if="anzahl !== null"
        class="text-sm text-gray-500 whitespace-nowrap"
        aria-live="polite"
      >
        {{ anzahl }} {{ anzahl === 1 ? einheit[0] : einheit[1] }}
        <template v-if="gesamt !== null && anzahl !== gesamt">von {{ gesamt }}</template>
      </span>
      <div class="flex items-center gap-2 sm:ml-auto">
        <Button
          v-if="hatAktiveFilter"
          v-tooltip.top="'Filter zurücksetzen'"
          icon="pi pi-filter-slash"
          aria-label="Filter zurücksetzen"
          severity="secondary"
          variant="text"
          @click="emit('zuruecksetzen')"
        />
        <Button
          label="Filter"
          icon="pi pi-sliders-h"
          :badge="anzahlFilter > 0 ? String(anzahlFilter) : undefined"
          severity="secondary"
          outlined
          @click="drawerVisible = true"
        />
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed, ref } from 'vue'
import Button from 'openvue/button'
import Drawer from 'openvue/drawer'
import IconField from 'openvue/iconfield'
import InputIcon from 'openvue/inputicon'
import InputText from 'openvue/inputtext'
import Listbox from 'openvue/listbox'
import Select from 'openvue/select'
import ToggleSwitch from 'openvue/toggleswitch'
import { sortierOptionen, sichtbarkeitOptionen } from '@/composables/sortierung'

const props = defineProps({
  suchLabel: {
    type: String,
    default: 'Suchen'
  },
  // Für Einträge ohne Sichtbarkeits-Flag (z. B. Gebiete) ausblenden
  mitSichtbarkeit: {
    type: Boolean,
    default: true
  },
  // Wenn gesetzt, wird ein Tag-Filter angezeigt
  tagOptionen: {
    type: Array,
    default: null
  },
  zusatzOptionen: {
    type: Array,
    default: () => []
  },
  anzahlFilter: {
    type: Number,
    default: 0
  },
  // Trefferanzeige "x Einträge von y"
  anzahl: {
    type: Number,
    default: null
  },
  gesamt: {
    type: Number,
    default: null
  },
  einheit: {
    type: Array,
    default: () => ['Eintrag', 'Einträge']
  }
})

const emit = defineEmits(['zuruecksetzen'])

const suche = defineModel('suche', { type: String, default: '' })
const sortierung = defineModel('sortierung', { type: String, default: 'name-auf' })
const sichtbarkeit = defineModel('sichtbarkeit', { type: String, default: 'alle' })
const tagIds = defineModel('tagIds', { type: Array, default: () => [] })
const zusatz = defineModel('zusatz', { type: Object, default: () => ({}) })

const drawerVisible = ref(false)

const optionen = computed(() =>
  props.mitSichtbarkeit
    ? sortierOptionen
    : sortierOptionen.filter((option) => option.value !== 'sichtbarkeit')
)

const hatAktiveFilter = computed(
  () => props.anzahlFilter > 0 || !!suche.value || sortierung.value !== 'name-auf'
)
</script>
