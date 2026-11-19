<template>
  <form @submit.prevent="onSubmit">
    <div class="mb-4">
      <FloatLabel variant="on" class="w-full">
        <InputText id="name" v-model="name" class="w-full" :invalid="!!errors.name" />
        <label for="name">Name des Gebiets</label>
      </FloatLabel>
      <small v-if="errors.name" id="name-help" class="p-error block">{{ errors.name }}</small>
    </div>
    <div class="flex justify-between items-center gap-2">
      <ButtonLoeschen v-if="props.editMode" outlined @delete-confirmed="onDelete" />
      <ButtonSpeichern type="submit" class="ml-auto" />
    </div>
  </form>
</template>

<script setup>
import { onMounted } from 'vue'
import { useForm } from 'vee-validate'
import { schema } from '@/utils/schemas/gemeindeGebiet'
import FloatLabel from 'openvue/floatlabel'
import InputText from 'openvue/inputtext'
import ButtonSpeichern from '@/components/ButtonSpeichern.vue'
import ButtonLoeschen from '@/components/ButtonLoeschen.vue'

const props = defineProps({
  editMode: {
    type: Boolean,
    default: false
  },
  item: {
    type: Object,
    required: false
  }
})

const { defineField, handleSubmit, errors, setValues, resetForm } = useForm({
  validationSchema: schema
})

onMounted(() => {
  if (props.editMode && props.item) {
    setValues({
      name: props.item.name
    })
  }
})

const [name] = defineField('name')

const emit = defineEmits(['add-item', 'update-item', 'delete-item'])

const onDelete = () => emit('delete-item', props.item.id)

const onSubmit = handleSubmit((values) => {
  if (props.editMode) {
    emit('update-item', { modelId: props.item.id, values })
  } else {
    emit('add-item', values)
  }
  resetForm()
})
</script>

<style></style>
