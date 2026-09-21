<template>
  <div>
    <form @submit.prevent="onSubmit">
      <div
        class="rounded-lg border overflow-hidden"
        :class="props.readOnly && tangiert ? 'border-blue-500' : 'border-gray-200'"
      >
        <!-- Header -->
        <div
          class="flex items-center justify-between gap-3 px-4 py-3 select-none"
          :class="{
            'bg-blue-500': props.readOnly && tangiert,
            'bg-gray-50': !props.readOnly || !tangiert,
            'cursor-pointer': !props.readOnly
          }"
          @click="!props.readOnly && setFieldValue('tangiert', !tangiert)"
        >
          <div class="flex items-center gap-3">
            <span
              class="w-7 h-7 rounded-full text-sm font-bold flex items-center justify-center flex-none"
              :class="props.readOnly && tangiert ? 'bg-white text-blue-600' : 'bg-blue-100 text-blue-700'"
            >
              {{ props.item.zielOber.nr }}
            </span>
            <span
              class="font-medium"
              :class="props.readOnly && tangiert ? 'text-white' : 'text-gray-800'"
            >{{ props.item.zielOber.name }}</span>
          </div>
          <ToggleSwitch v-model="tangiert" @click.stop :invalid="!!errors.tangiert" :disabled="props.readOnly" />
        </div>

        <!-- Unter-Ziele -->
        <div v-if="tangiert" class="divide-y divide-gray-100">
          <div
            v-for="(eingabeZielUnter, index) in props.item.eingabeZielUnter"
            :key="eingabeZielUnter.id"
          >
            <MobilitaetscheckFormularEingabeZielUnterItem
              :editMode="props.editMode"
              :readOnly="props.readOnly"
              :item="eingabeZielUnter"
              :zielOberNr="props.item.zielOber.nr"
              :ref="(el) => registerUnterRef(el, index)"
            />
          </div>
        </div>
      </div>
    </form>
  </div>
</template>

<script setup>
import { onMounted, ref, watch } from 'vue'
import { useForm } from 'vee-validate'
import { updateItemSilent } from '@/composables/crud'
import { useDebounceFn } from '@vueuse/core'
import { schema } from '@/utils/schemas/mobilitaetscheckEingabeZielOber'
import ToggleSwitch from 'openvue/toggleswitch'
import MobilitaetscheckFormularEingabeZielUnterItem from '@/components/MobilitaetscheckFormularEingabeZielUnterItem.vue'

const mobilitaetscheckFormularEingabeZielUnterRefs = ref([])

const registerUnterRef = (el, index) => {
  if (el) mobilitaetscheckFormularEingabeZielUnterRefs.value[index] = el
}

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
  }
})

const { defineField, handleSubmit, validate, errors, setFieldValue, setValues } = useForm({
  validationSchema: schema
})

const [tangiert] = defineField('tangiert')
const isInitialized = ref(false)

onMounted(() => {})

watch(
  () => props.item,
  (newItem) => {
    if (!newItem) return
    const { tangiert, eingabeId, zielOberId } = props.item
    setValues({
      tangiert,
      eingabeId,
      zielOberId
    })
    isInitialized.value = true
  },
  { immediate: true }
)

const autoSave = useDebounceFn(async () => {
  if (!isInitialized.value || props.readOnly) return
  await updateItemSilent({
    model: 'mobilitaetscheck/eingabe/ziel/ober',
    modelId: props.item.id,
    values: {
      tangiert: tangiert.value,
      eingabeId: props.item.eingabeId,
      zielOberId: props.item.zielOberId
    }
  })
}, 1500)

watch([tangiert], autoSave)

const onSubmit = handleSubmit(async (values) => {
  const refs = mobilitaetscheckFormularEingabeZielUnterRefs.value.filter((ref) => ref)

  // Step 1: Validate all sub-forms
  const validationResults = await Promise.all(refs.map((ref) => ref.validate?.()))
  const allValid = validationResults.every((result) => result?.valid === true)

  if (!allValid) {
    return false
  }

  await updateItemSilent({
    model: 'mobilitaetscheck/eingabe/ziel/ober',
    modelId: props.item.id,
    values
  })
  // Step 3: Submit all sub-forms
  await Promise.all(refs.map((ref) => ref.onSubmit?.()))
  return true
})

defineExpose({ onSubmit, validate })
</script>

<style scoped></style>
