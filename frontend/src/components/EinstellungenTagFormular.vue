<template>
  <form @submit.prevent="onSubmit">
    <div class="grid grid-cols-1 gap-4 items-center">
      <div class="w-full">
        <FloatLabel variant="on" class="w-full">
          <InputText id="name" v-model="name" class="w-full" :invalid="!!errors.name" />
          <label for="name">Tag eingeben</label>
        </FloatLabel>
        <small v-if="errors.name" id="name-help" class="p-error block">{{ errors.name }}</small>
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
import { schema } from '@/utils/schemas/tag'
import FloatLabel from 'openvue/floatlabel'
import InputText from 'openvue/inputtext'
import ButtonSpeichern from '@/components/ButtonSpeichern.vue'
import ButtonLoeschen from '@/components/ButtonLoeschen.vue'
import FeldSichtbarkeitAndereKommunen from '@/components/FeldSichtbarkeitAndereKommunen.vue'

const props = defineProps({
  editMode: {
    type: Boolean,
    required: true
  },
  item: Object
})

const { defineField, handleSubmit, errors, setValues } = useForm({
  validationSchema: schema,
  initialValues: { gemeindespezifisch: false }
})

const [name] = defineField('name')
const [gemeindespezifisch] = defineField('gemeindespezifisch')

onMounted(() => {
  if (props.editMode) {
    setValues({
      name: props.item.name,
      gemeindespezifisch: props.item.gemeindespezifisch ?? false
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
