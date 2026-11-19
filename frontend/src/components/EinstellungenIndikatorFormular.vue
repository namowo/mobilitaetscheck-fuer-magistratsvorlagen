<template>
  <form @submit.prevent="onSubmit">
    <div class="grid grid-cols-1 gap-2">
      <div class="grid grid-cols-1 gap-3">
        <div class="w-full">
          <FloatLabel variant="on" class="w-full">
            <InputText id="name" v-model="name" class="w-full" :invalid="!!errors.name" />
            <label for="name">Indikator-Bezeichnung</label>
          </FloatLabel>
          <small v-if="errors.name" id="name-help" class="p-error block">{{ errors.name }}</small>
        </div>
        <div class="w-full">
          <FloatLabel variant="on" class="w-full">
            <InputText
              id="quelleUrl"
              v-model.trim="quelleUrl"
              class="w-full"
              :invalid="!!errors.quelleUrl"
            />
            <label for="quelleUrl">Quellen-URL <LabelOptional /></label>
          </FloatLabel>
          <small v-if="errors.quelleUrl" id="quelleUrl-help" class="p-error block">{{
            errors.quelleUrl
          }}</small>
        </div>
        <FloatLabel variant="on">
          <MultiSelect
            id="tags"
            v-model="tagIds"
            :options="props.tags"
            optionLabel="name"
            optionValue="id"
            display="chip"
            class="w-full"
          />
          <label for="tags">Tags auswählen <LabelOptional /></label>
        </FloatLabel>
      </div>
      <FeldSichtbarkeitAndereKommunen v-model="gemeindespezifisch" />
      <div class="flex justify-between items-center gap-2">
        <ButtonLoeschen v-if="props.editMode" outlined @delete-confirmed="onDelete" />
        <ButtonSpeichern type="submit" class="ml-auto" />
      </div>
    </div>
  </form>
</template>

<script setup>
import { onMounted } from 'vue'
import { useForm } from 'vee-validate'
import { schema } from '@/utils/schemas/indikator.js'
import FloatLabel from 'openvue/floatlabel'
import InputText from 'openvue/inputtext'
import MultiSelect from 'openvue/multiselect'
import ButtonSpeichern from '@/components/ButtonSpeichern.vue'
import ButtonLoeschen from '@/components/ButtonLoeschen.vue'
import FeldSichtbarkeitAndereKommunen from '@/components/FeldSichtbarkeitAndereKommunen.vue'

const props = defineProps({
  editMode: {
    type: Boolean,
    required: true
  },
  item: {
    type: Object,
    default: null
  },
  tags: Array
})

const { defineField, handleSubmit, errors, setValues } = useForm({
  validationSchema: schema,
  initialValues: { gemeindespezifisch: false }
})

const [name] = defineField('name')
const [gemeindespezifisch] = defineField('gemeindespezifisch')
const [quelleUrl] = defineField('quelleUrl')
const [tagIds] = defineField('tagIds')

onMounted(() => {
  if (props.editMode) {
    setValues({
      name: props.item.name,
      gemeindespezifisch: props.item.gemeindespezifisch ?? false,
      tagIds: props.item.tagIds,
      quelleUrl: props.item.quelleUrl
    })
  }
})

const emit = defineEmits(['add-item', 'update-item', 'delete-item'])

const onDelete = () => emit('delete-item', props.item.id)

const onSubmit = handleSubmit(async (values) => {
  if (props.editMode) {
    emit('update-item', { modelId: props.item.id, values })
  } else {
    emit('add-item', values)
  }
})
</script>

<style scoped>
.p-invalid {
  @apply border-red-600 text-red-600;
}

.p-error {
  @apply text-red-600;
}
</style>
