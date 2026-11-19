<template>
  <form @submit.prevent="onSubmit">
    <div class="grid grid-cols-1 gap-4">
      <div>
        <label for="name" class="block mb-1 text-sm font-medium text-gray-700">Textbaustein</label>
        <Editor
          id="name"
          v-model="name"
          :invalid="!!errors.name"
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
        <small v-if="errors.name" id="name-help" class="p-error block">{{ errors.name }}</small>
      </div>
      <div>
        <FloatLabel variant="on">
          <MultiSelect
            id="tags"
            v-model="tagIds"
            :options="props.tags"
            optionLabel="name"
            optionValue="id"
            display="chip"
            class="w-full"
            :invalid="!!errors.tagIds"
          />
          <label for="tags">Tags auswählen <LabelOptional /></label>
        </FloatLabel>
        <small v-if="errors.tagIds" id="name-help" class="p-error block">{{ errors.tagIds }}</small>
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
import { schema } from '@/utils/schemas/textblock.js'
import FloatLabel from 'openvue/floatlabel'
import Editor from 'openvue/editor'
import MultiSelect from 'openvue/multiselect'
import ButtonSpeichern from '@/components/ButtonSpeichern.vue'
import ButtonLoeschen from '@/components/ButtonLoeschen.vue'
import FeldSichtbarkeitAndereKommunen from '@/components/FeldSichtbarkeitAndereKommunen.vue'

const props = defineProps({
  editMode: {
    type: Boolean,
    required: true
  },
  item: Object,
  tags: Array
})

const { defineField, handleSubmit, errors, setValues } = useForm({
  validationSchema: schema,
  initialValues: { gemeindespezifisch: false }
})

const [name] = defineField('name')
const [gemeindespezifisch] = defineField('gemeindespezifisch')
const [tagIds] = defineField('tagIds')

onMounted(() => {
  if (props.editMode) {
    setValues({
      name: props.item.name,
      gemeindespezifisch: props.item.gemeindespezifisch ?? false,
      tagIds: props.item.tagIds
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
