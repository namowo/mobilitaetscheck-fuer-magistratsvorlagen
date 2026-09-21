<template>
  <div>
    <Message v-if="hasErrors" severity="error" class="mb-4">
      <ul class="list-disc list-inside">
        <li v-for="(error, field) in errors" :key="field">{{ error }}</li>
      </ul>
    </Message>
    <form @submit.prevent="onSubmit" class="mt-4">
      <Stepper value="1">
        <StepList>
          <Step value="1"></Step>
          <Step value="2"></Step>
        </StepList>
        <StepPanels>
          <StepPanel v-slot="{ activateCallback }" value="1">
            <ol>
              <li>
                <span>
                  Hat Ihr Vorhaben abweichend von den bisherigen Aspekten eine positive
                  Klimarelevanz?
                </span>
                <SelectButton
                  v-model="d1q1"
                  :options="optionBoolean"
                  optionLabel="name"
                  optionValue="id"
                  :multiple="false"
                  :invalid="!!errors.d1q1"
                  class="mt-2"
                />
              </li>
              <li v-if="d1q1 === 1">
                <span>
                  Bitte begründen Sie im Folgenden, inwiefern Ihr Vorhaben eine positive
                  Klimarelevanz hat.
                </span>
                <FloatLabel variant="on" class="w-full mt-2">
                  <InputText
                    id="d1q2"
                    v-model="d1q2"
                    aria-describedby="d1q2-help"
                    :invalid="!!errors.d1q2"
                    class="w-full"
                    inputClass="w-full"
                  />
                  <label for="d1q2">Begründung</label>
                </FloatLabel>
              </li>
            </ol>

            <div class="flex pt-6 justify-end">
              <Button
                label="Weiter"
                icon="pi pi-arrow-right"
                iconPos="right"
                @click="activateCallback('2')"
              />
            </div>
          </StepPanel>
          <StepPanel v-slot="{ activateCallback }" value="2">
            <ol>
              <li>
                <span>
                  Hat Ihr Vorhaben abweichend von den bisherigen Aspekten eine negative
                  Klimarelevanz?
                </span>
                <SelectButton
                  v-model="d2q1"
                  :options="optionBoolean"
                  optionLabel="name"
                  optionValue="id"
                  :multiple="false"
                  :invalid="!!errors.d2q1"
                  class="mt-2"
                />
              </li>
              <li v-if="d2q1 === 1">
                <span>
                  Bitte begründen Sie im Folgenden, inwiefern Ihr Vorhaben eine negative
                  Klimarelevanz hat.
                </span>
                <FloatLabel variant="on" class="w-full mt-2">
                  <InputText
                    id="d2q2"
                    v-model="d2q2"
                    aria-describedby="d2q2-help"
                    :invalid="!!errors.d2q2"
                    class="w-full"
                    inputClass="w-full"
                  />
                  <label for="d2q2">Begründung</label>
                </FloatLabel>
              </li>
            </ol>
            <div class="flex pt-6 justify-between">
              <Button
                label="Zurück"
                severity="secondary"
                icon="pi pi-arrow-left"
                @click="activateCallback('1')"
              />
              <Button label="Speichern" type="submit" icon="pi pi-save" iconPos="right" />
            </div>
          </StepPanel>
        </StepPanels>
      </Stepper>
    </form>
  </div>
</template>

<script setup>
import { computed, onMounted, ref } from 'vue'
import { useForm } from 'vee-validate'
import { schema } from '@/utils/schemas/klimarelevanzpruefungEingabeFb4'
import { createItemSilent, fetchItems, updateItemSilent } from '@/composables/crud'
import Button from 'openvue/button'
import InputText from 'openvue/inputtext'
import FloatLabel from 'openvue/floatlabel'
import SelectButton from 'openvue/selectbutton'
import Stepper from 'openvue/stepper'
import StepList from 'openvue/steplist'
import StepPanels from 'openvue/steppanels'
import Step from 'openvue/step'
import StepPanel from 'openvue/steppanel'
import Message from 'openvue/message'

const optionBoolean = ref()

const props = defineProps({
  editMode: {
    type: Boolean,
    default: false
  },
  item: {
    type: Object,
    default: null
  }
})

onMounted(async () => {
  optionBoolean.value = await fetchItems('/einstellungen/bool-erweitert')
  if (props.editMode && props.item) {
    setValues(props.item)
  }
})

const { defineField, handleSubmit, errors, setValues, values } = useForm({
  validationSchema: schema
})

const hasErrors = computed(() => Object.keys(errors.value).length > 0)

const [d1q1] = defineField('d1q1')
const [d1q2] = defineField('d1q2')
const [d2q1] = defineField('d2q1')
const [d2q2] = defineField('d2q2')

const currentItemId = ref(props.item?.id ?? null)
const alreadySaved = ref(false)

const emit = defineEmits(['update-item', 'add-item'])

const triggerDraftSave = async () => {
  if (alreadySaved.value) return null
  const snapshot = { ...values }
  const hasData = Object.values(snapshot).some((v) => v !== null && v !== undefined)
  if (!hasData) return null
  const draftValues = { ...snapshot, fertig: false }
  if (currentItemId.value) {
    const response = await updateItemSilent({
      model: 'klimarelevanzpruefung/eingabe/fb4',
      modelId: currentItemId.value,
      values: draftValues
    })
    return response ?? null
  } else {
    const response = await createItemSilent({
      model: 'klimarelevanzpruefung/eingabe/fb4',
      values: draftValues
    })
    if (response) {
      currentItemId.value = response.id
      return response
    }
    return null
  }
}

defineExpose({ triggerDraftSave })

const onSubmit = handleSubmit(async (validatedValues) => {
  alreadySaved.value = true
  const fullValues = { ...validatedValues, fertig: true }
  if (currentItemId.value) {
    emit('update-item', { fb: 4, modelId: currentItemId.value, values: fullValues })
  } else {
    emit('add-item', { fb: 4, values: fullValues })
  }
})
</script>

<style scoped>
ol {
  counter-reset: question;
  list-style: none;
  padding-left: 0;
}

ol > li {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  counter-increment: question;
  margin-bottom: 1rem;
}

ol > li > span:first-child::before {
  content: counter(question) '. ';
  font-weight: bold;
}
</style>
