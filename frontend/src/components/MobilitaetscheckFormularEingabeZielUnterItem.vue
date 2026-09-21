<template>
  <form @submit.prevent="onSubmit">
    <div
      class="px-4 py-3"
      :class="props.readOnly && tangiert ? 'border-l-4 border-blue-500 bg-blue-50' : ''"
    >
      <!-- Header -->
      <div
        class="flex items-center justify-between gap-3 select-none"
        :class="{ 'cursor-pointer': !props.readOnly }"
        @click="!props.readOnly && setFieldValue('tangiert', !tangiert)"
      >
        <div class="flex items-center gap-2 min-w-0">
          <span
            class="text-sm font-medium flex-none tabular-nums"
            :class="props.readOnly && tangiert ? 'text-blue-600' : 'text-gray-400'"
          >
            {{ props.zielOberNr }}.{{ item.zielUnter.nr }}
          </span>
          <span
            class="text-sm font-medium truncate"
            :class="props.readOnly && tangiert ? 'text-blue-900' : 'text-gray-700'"
            >{{ item.zielUnter.name }}</span
          >
        </div>
        <ToggleSwitch
          v-model="tangiert"
          @click.stop
          :invalid="!!errors.tangiert"
          :disabled="props.readOnly"
          class="flex-none"
        />
      </div>

      <!-- Felder wenn tangiert — READ ONLY: strukturierter Text -->
      <div v-if="tangiert && props.readOnly" class="mt-3 flex flex-col gap-3 pl-3 text-sm">
        <div class="grid grid-cols-2 gap-4">
          <div>
            <p class="text-xs font-semibold text-blue-700 uppercase tracking-wide mb-1">
              Wirkungsrichtung und -stärke
            </p>
            <span
              class="px-3 py-1 rounded-full text-sm font-medium inline-block"
              :style="{
                backgroundColor: auswirkungDisplay.bg ?? '#f3f4f6',
                color: auswirkungDisplay.color,
                border: auswirkungDisplay.border ? '1px solid #d1d5db' : 'none'
              }"
              >{{ auswirkungDisplay.label }}</span
            >
          </div>
          <div v-if="auswirkungRaeumlichLabel">
            <p class="text-xs font-semibold text-blue-700 uppercase tracking-wide mb-1">
              Räumliche Auswirkung
            </p>
            <span class="flex items-center gap-1.5 text-gray-800">
              <i :class="auswirkungRaeumlichIcon" class="text-blue-600" />
              {{ auswirkungRaeumlichLabel }}
            </span>
          </div>
        </div>
        <div v-if="anmerkung">
          <p class="text-xs font-semibold text-blue-700 uppercase tracking-wide mb-0.5">
            Erläuterung
          </p>
          <p class="text-gray-800 whitespace-pre-wrap">{{ anmerkung }}</p>
        </div>
        <div v-if="indikatoren.length">
          <p class="text-xs font-semibold text-blue-700 uppercase tracking-wide mb-0.5">
            Indikatoren
          </p>
          <div class="flex flex-wrap gap-1 mt-1">
            <a
              v-for="ind in indikatoren"
              :key="ind.id"
              :href="ind.quelleUrl || undefined"
              :target="ind.quelleUrl ? '_blank' : undefined"
              :rel="ind.quelleUrl ? 'noopener noreferrer' : undefined"
              class="px-2 py-0.5 bg-blue-600 text-white text-xs rounded-full font-medium"
              :class="
                ind.quelleUrl ? 'hover:bg-blue-200 underline cursor-pointer' : 'cursor-default'
              "
              >{{ ind.name }}</a
            >
          </div>
        </div>
      </div>

      <!-- Felder wenn tangiert — EDIT MODE: Eingabefelder -->
      <div v-else-if="tangiert" class="mt-4 flex flex-col gap-4 pl-4 border-l-2 border-blue-100">
        <div class="grid grid-cols-2 gap-4">
          <div class="w-full max-w-md pl-6">
            <label for="auswirkung" class="text-sm text-gray-600"
              >Wirkungsrichtung und -stärke</label
            >
            <div class="relative mt-3 mb-6">
              <Slider
                id="auswirkung"
                v-model.number="auswirkung"
                :min="-3"
                :max="3"
                :step="1"
                :invalid="!!errors.auswirkung"
                class="w-full"
                :key="sliderKey"
                :pt="{
                  root: { style: 'height: 2px; background: #d1d5db; border-radius: 2px' },
                  range: { style: 'display: none' },
                  handle: {
                    style:
                      'width: 1.25rem; height: 1.25rem; margin-top: -0.625rem; margin-left: -0.625rem; cursor: pointer;  background: #507c96;z-index: 10'
                  }
                }"
              />
              <!-- Tick-Striche: absolut positioniert wie Slider-Steps (i/6 * 100%) -->
              <div class="absolute inset-x-0" style="top: -5px">
                <span
                  v-for="(tick, i) in 7"
                  :key="tick"
                  class="absolute flex flex-col items-center cursor-pointer -translate-x-1/2"
                  :style="{ left: `${(i / 6) * 100}%` }"
                  @click="moveSlider(i - 3)"
                >
                  <span class="w-px h-3 bg-gray-400 block"></span>
                  <span class="mt-1 text-xs text-gray-500 whitespace-nowrap">
                    {{ tickmarkLabels[tick] }}
                  </span>
                </span>
              </div>
            </div>
          </div>
          <div class="my-auto max-w-md">
            <FloatLabel variant="on">
              <Select
                id="auswirkungRaeumlichId"
                v-model="auswirkungRaeumlichId"
                :options="optionsAuswirkungRaeumlich"
                optionLabel="name"
                optionValue="id"
                :invalid="!!errors.auswirkungRaeumlichId"
                class="w-full dont-close-on-select"
              />
              <label for="auswirkungRaeumlichId">Räumliche Auswirkung</label>
            </FloatLabel>
          </div>
        </div>

        <div class="max-w-5xl">
          <label for="anmerkung">Erläuterung</label>
          <Editor
            id="anmerkung"
            v-model="anmerkung"
            rows="5"
            :invalid="!!errors.anmerkung"
            class="w-full"
            editorStyle="min-height: 160px"
          >
            <template #toolbar>
              <span class="ql-formats">
                <button v-tooltip.bottom="'Fett'" class="ql-bold"></button>
                <button v-tooltip.bottom="'Kursiv'" class="ql-italic"></button>
                <button v-tooltip.bottom="'Unterstrichen'" class="ql-underline"></button>
                <button v-tooltip.bottom="'Durchgestrichen'" class="ql-strike"></button>
              </span>
              <span class="ql-formats">
                <button
                  v-tooltip.bottom="'Nummerierte Liste'"
                  class="ql-list"
                  value="ordered"
                ></button>
                <button v-tooltip.bottom="'Liste'" class="ql-list" value="bullet"></button>
              </span>
              <span class="ql-formats">
                <button v-tooltip.bottom="'Link'" class="ql-link"></button>
              </span>
              <span class="ql-formats">
                <button v-tooltip.bottom="'Formatierung entfernen'" class="ql-clean"></button>
              </span>
            </template>
          </Editor>
        </div>

        <ButtonTextblockHinzufuegen
          v-if="!isPolitik"
          class="w-full"
          @textblock-hinzufuegen="textblockHinzufuegen($event)"
        />

        <div class="max-w-5xl">
          <FloatLabel variant="on">
            <MultiSelect
              id="indikatoren"
              v-model="indikatorIds"
              :options="optionsIndikatoren"
              filter
              optionLabel="name"
              optionValue="id"
              class="w-full dont-close-on-select"
              display="chip"
              :invalid="!!errors.indikatorIds"
              empty-filter-message="Keine Ergebnisse gefunden"
              :pt="{
                header: () => ({
                  id: `indicators_header`
                })
              }"
            />
            <label for="indikatoren">Indikatoren auswählen</label>
          </FloatLabel>
        </div>
      </div>
    </div>
  </form>
</template>

<script setup>
import { ref, computed, onMounted, watch, nextTick } from 'vue'
import { useStorage, useDebounceFn } from '@vueuse/core'
import { fetchItem, fetchItems, updateItemSilent } from '@/composables/crud'
import { useAuthStore } from '@/stores/auth'
import { useForm } from 'vee-validate'
import { schema } from '@/utils/schemas/mobilitaetscheckEingabeZielUnter'
import Editor from 'openvue/editor'
import ToggleSwitch from 'openvue/toggleswitch'
import FloatLabel from 'openvue/floatlabel'
import Select from 'openvue/select'
import MultiSelect from 'openvue/multiselect'
import Textarea from 'openvue/textarea'
import Slider from 'openvue/slider'
import ButtonTextblockHinzufuegen from '@/components/ButtonTextblockHinzufuegen.vue'

const authStore = useAuthStore()
const isPolitik = computed(() => authStore.userRolleId === 2)

const props = defineProps({
  editMode: {
    type: Boolean,
    default: false
  },
  readOnly: {
    type: Boolean,
    default: false
  },
  item: {
    type: Object,
    default: null
  },
  zielOberNr: {
    type: Number
  }
})

const optionsIndikatoren = ref([])
const tickmarkLabels = useStorage('cachedTickmarkLabels', {})
const optionsAuswirkungRaeumlich = useStorage('cachedAuswirkungRaeumlich', [])
const sliderKey = ref(0)
const isInitialized = ref(false)

const fetchOptions = async () => {
  if (
    !Array.isArray(optionsAuswirkungRaeumlich.value) ||
    optionsAuswirkungRaeumlich.value.length === 0
  ) {
    optionsAuswirkungRaeumlich.value = await fetchItems(
      '/option/mobilitaetscheck/auswirkung-raeumlich'
    )
  }
  if (Object.keys(tickmarkLabels.value).length === 0) {
    tickmarkLabels.value = await fetchItem('/option/mobilitaetscheck/auswirkung-tickmarks')
  }
  optionsIndikatoren.value = await fetchItems('/einstellungen/indikator')
}

const { defineField, handleSubmit, validate, errors, setFieldValue, setValues } = useForm({
  validationSchema: schema
})

const [tangiert] = defineField('tangiert')
const [auswirkung] = defineField('auswirkung')
const [auswirkungRaeumlichId] = defineField('auswirkungRaeumlichId')
const [anmerkung] = defineField('anmerkung')
const [indikatorIds] = defineField('indikatorIds')

const auswirkungDisplay = computed(() => {
  const v = auswirkung.value
  if (v === null || v === undefined) return { label: 'keine Angabe', bg: null, color: '#374151' }
  if (v < -2.5) return { label: 'stark negativ', bg: 'rgb(255,16,16)', color: 'white' }
  if (v <= -1.5) return { label: 'negativ', bg: 'rgb(255,95,95)', color: 'white' }
  if (v < 0) return { label: 'leicht negativ', bg: 'rgb(255,175,175)', color: '#7f1d1d' }
  if (v === 0) return { label: 'neutral', bg: 'rgb(255,255,255)', color: '#374151', border: true }
  if (v <= 1.5) return { label: 'leicht positiv', bg: 'rgb(176,222,171)', color: '#14532d' }
  if (v <= 2.5) return { label: 'positiv', bg: 'rgb(97,189,88)', color: 'white' }
  return { label: 'stark positiv', bg: 'rgb(18,157,5)', color: 'white' }
})

const auswirkungRaeumlichLabel = computed(() => {
  if (!auswirkungRaeumlichId.value) return null
  return (
    optionsAuswirkungRaeumlich.value.find((o) => o.id === auswirkungRaeumlichId.value)?.name ??
    props.item?.auswirkungRaeumlich?.name ??
    null
  )
})

const RAEUMLICH_ICONS = {
  lokal: 'pi pi-map-marker',
  quartiersweit: 'pi pi-th-large',
  stadtweit: 'pi pi-globe'
}

const auswirkungRaeumlichIcon = computed(() => {
  return RAEUMLICH_ICONS[auswirkungRaeumlichLabel.value] ?? 'pi pi-map'
})

const indikatoren = computed(() => {
  if (!indikatorIds.value?.length) return []
  if (optionsIndikatoren.value.length === 0) return props.item?.indikatoren ?? []
  return indikatorIds.value
    .map((id) => optionsIndikatoren.value.find((o) => o.id === id))
    .filter(Boolean)
})

onMounted(async () => {
  if (!props.readOnly) await fetchOptions()
})

watch(
  () => props.item,
  async (newItem) => {
    if (!newItem) return
    const {
      tangiert,
      auswirkung,
      auswirkungRaeumlichId,
      anmerkung,
      indikatorIds,
      eingabeZielOberId,
      zielUnterId
    } = newItem

    setValues({
      tangiert,
      auswirkung,
      auswirkungRaeumlichId,
      anmerkung,
      indikatorIds,
      eingabeZielOberId,
      zielUnterId
    })

    // Force slider to re-render with new value
    await nextTick()
    sliderKey.value++
    isInitialized.value = true
  },
  { immediate: true }
)

const autoSave = useDebounceFn(async () => {
  if (!isInitialized.value || props.readOnly) return
  await updateItemSilent({
    model: 'mobilitaetscheck/eingabe/ziel/unter',
    modelId: props.item.id,
    values: {
      tangiert: tangiert.value,
      auswirkung: auswirkung.value ?? 0,
      auswirkungRaeumlichId: auswirkungRaeumlichId.value,
      anmerkung: anmerkung.value,
      indikatorIds: indikatorIds.value ?? [],
      eingabeZielOberId: props.item.eingabeZielOberId,
      zielUnterId: props.item.zielUnterId
    }
  })
}, 1500)

watch([tangiert, auswirkung, auswirkungRaeumlichId, anmerkung, indikatorIds], autoSave)

const moveSlider = (tickValue) => {
  setFieldValue('auswirkung', tickValue)
}

const textblockHinzufuegen = (event) => {
  const current = anmerkung?.value?.trim()

  if (current && current.length > 0) {
    setFieldValue('anmerkung', `${anmerkung.value}\n${event}`)
  } else {
    setFieldValue('anmerkung', event)
  }
}

const onSubmit = handleSubmit(async (values) => {
  await updateItemSilent({
    model: 'mobilitaetscheck/eingabe/ziel/unter',
    modelId: props.item.id,
    values
  })
})

defineExpose({ onSubmit, validate })
</script>

<style scoped>
:deep(.p-slider:hover .p-slider-handle) {
  transform: scale(1.1);
  transition: transform 0.2s ease;
}
</style>
