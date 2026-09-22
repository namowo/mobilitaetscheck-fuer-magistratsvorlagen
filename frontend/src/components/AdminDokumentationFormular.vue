<template>
  <form @submit.prevent="onSubmit">
    <div class="grid grid-cols-1 gap-3">
      <div class="w-full">
        <FloatLabel variant="on" class="w-full">
          <InputText id="titel" v-model="titel" class="w-full" :invalid="!!errors.titel" @input="onTitelInput" />
          <label for="titel">Titel</label>
        </FloatLabel>
        <small v-if="errors.titel" class="p-error block">{{ errors.titel }}</small>
      </div>
      <div class="w-full">
        <FloatLabel variant="on" class="w-full">
          <InputText id="slug" v-model="slug" class="w-full" :invalid="!!errors.slug" @input="slugEditedManually = true" />
          <label for="slug">Anker (URL-Slug)</label>
        </FloatLabel>
        <small v-if="errors.slug" class="p-error block">{{ errors.slug }}</small>
      </div>
      <div class="flex items-center gap-3">
        <ToggleSwitch v-model="zeigtKontaktButton" inputId="zeigtKontaktButton" />
        <label for="zeigtKontaktButton" class="text-sm">Kontakt-Button anzeigen</label>
      </div>
      <Message v-if="zeigtKontaktButton" severity="info">
        Unterhalb des Inhalts wird auf der öffentlichen Seite zusätzlich ein „Kontakt
        aufnehmen"-Button angezeigt, der die hinterlegte Kontakt-E-Mail-Adresse verwendet. Der
        Button ist kein Teil des hier bearbeitbaren Inhalts.
      </Message>
      <div class="w-full">
        <label class="block text-sm text-gray-500 mb-1">Inhalt</label>
        <RichContentEditor v-model="inhaltModel" />
      </div>
      <div class="flex justify-end items-center">
        <ButtonSpeichern type="submit" />
      </div>
    </div>
  </form>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useForm } from 'vee-validate'
import { schema } from '@/utils/schemas/dokumentationSeite'
import FloatLabel from 'openvue/floatlabel'
import InputText from 'openvue/inputtext'
import Message from 'openvue/message'
import ToggleSwitch from 'openvue/toggleswitch'
import ButtonSpeichern from '@/components/ButtonSpeichern.vue'
import RichContentEditor from '@/components/RichContentEditor.vue'

const props = defineProps({
  editMode: {
    type: Boolean,
    required: true
  },
  item: Object
})

const { defineField, handleSubmit, errors, setValues, setFieldValue, values } = useForm({
  validationSchema: schema
})

const [titel] = defineField('titel')
const [slug] = defineField('slug')
const [inhaltModel] = defineField('inhalt')
const [zeigtKontaktButton] = defineField('zeigtKontaktButton')

const slugEditedManually = ref(false)

const slugify = (value) =>
  (value || '')
    .toLowerCase()
    .trim()
    .replace(/[äöüß]/g, (c) => ({ ä: 'ae', ö: 'oe', ü: 'ue', ß: 'ss' })[c])
    .replace(/[^a-z0-9]+/g, '-')
    .replace(/^-+|-+$/g, '')

const onTitelInput = () => {
  if (!slugEditedManually.value) {
    setFieldValue('slug', slugify(values.titel))
  }
}

onMounted(() => {
  if (props.editMode) {
    slugEditedManually.value = true
    setValues({
      titel: props.item.titel,
      slug: props.item.slug,
      inhalt: props.item.inhalt || '',
      zeigtKontaktButton: props.item.zeigtKontaktButton || false
    })
  } else {
    setFieldValue('zeigtKontaktButton', false)
  }
})

const emit = defineEmits(['add-item', 'update-item'])

const onSubmit = handleSubmit(async (formValues) => {
  if (props.editMode) {
    emit('update-item', { modelId: props.item.id, values: formValues })
  } else {
    emit('add-item', formValues)
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
