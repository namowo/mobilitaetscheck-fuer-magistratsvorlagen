<template>
  <div>
    <BaseSpinner v-if="isLoadingData" />
    <div
      v-else-if="!hasStandard"
      class="my-7 p-4 bg-yellow-50 border border-yellow-300 rounded flex flex-col gap-2"
    >
      <p class="text-yellow-800 font-medium">Kein Standard-Leitziele konfiguriert</p>
      <p class="text-yellow-700 text-sm">
        Bevor ein Mobilitätscheck erstellt werden kann, muss zunächst ein
        <RouterLink :to="{ name: 'leitziel-sets' }" class="underline hover:text-yellow-900">
          Standard-Leitziele eingestellt
        </RouterLink>
        werden.
      </p>
    </div>

    <form v-else class="grid grid-cols-1 gap-y-4 my-7" @submit.prevent="onSubmit">
      <div class="form-group field">
        <FloatLabel variant="on">
          <InputText
            id="name"
            v-model="name"
            aria-describedby="name-help"
            :invalid="!!errors.name"
            class="w-full"
            inputClass="w-full"
          />
          <label for="name">Name des Mobilitätschecks</label>
        </FloatLabel>
        <small v-if="errors.name" id="name-help" class="p-error block">{{ errors.name }}</small>
      </div>

      <div v-if="!isPolitik" class="form-group field">
        <label for="zielSetId" class="block mb-1 font-medium text-sm">Leitziele *</label>
        <Select
          id="zielSetId"
          v-model="zielSetId"
          :options="eigeneSets"
          optionLabel="name"
          optionValue="id"
          :invalid="!!errors.zielSetId"
          placeholder="Bitte wählen..."
          class="w-full"
        >
          <template #option="{ option }">
            <div class="flex items-center gap-2">
              <span>{{ option.name }}</span>
              <span
                v-if="option.istStandard"
                class="text-xs bg-yellow-100 text-yellow-700 px-2 py-0.5 rounded-full"
              >
                Standard
              </span>
            </div>
          </template>
        </Select>
        <small v-if="errors.zielSetId" id="zielSetId-help" class="p-error block">{{
          errors.zielSetId
        }}</small>
      </div>

      <div class="flex justify-end w-full">
        <ButtonSpeichern type="submit" :loading="isSubmitting">Mobilitätscheck anlegen</ButtonSpeichern>
      </div>
    </form>
  </div>
</template>

<script setup>
import { computed, onMounted, ref } from 'vue'
import { RouterLink, useRoute, useRouter } from 'vue-router'
import { useForm } from 'vee-validate'
import { schema } from '@/utils/schemas/mobilitaetscheckEingabe'
import { toTypedSchema } from '@vee-validate/yup'
import { createItem, fetchItems } from '@/composables/crud'
import { useAuthStore } from '@/stores/auth'
import InputText from 'openvue/inputtext'
import FloatLabel from 'openvue/floatlabel'
import Select from 'openvue/select'
import ButtonSpeichern from '@/components/ButtonSpeichern.vue'
import BaseSpinner from '@/components/BaseSpinner.vue'

const route = useRoute()
const router = useRouter()
const authStore = useAuthStore()
const isLoadingData = ref(true)
const isSubmitting = ref(false)
const zielSets = ref([])
const isPolitik = computed(() => authStore.userRolleId === 2)
const eigeneSets = computed(() => zielSets.value.filter((s) => s.gemeindeId === authStore.gemeindeId))
const hasStandard = computed(() => zielSets.value.some((s) => s.istStandard))

const { defineField, handleSubmit, errors, setFieldValue } = useForm({
  validationSchema: toTypedSchema(schema)
})

const [name] = defineField('name')
const [zielSetId] = defineField('zielSetId')

setFieldValue('magistratsvorlageId', route.params.id)

onMounted(async () => {
  const data = await fetchItems('/einstellungen/mobilitaetscheck/ziel-set')
  zielSets.value = Array.isArray(data) ? data : []

  // Pre-select the standard set if one is configured
  const standardSet = zielSets.value.find((s) => s.istStandard)
  if (standardSet) {
    setFieldValue('zielSetId', standardSet.id)
  }
  isLoadingData.value = false
})

const onSubmit = handleSubmit(async (values) => {
  isSubmitting.value = true
  const response = await createItem({
    model: 'mobilitaetscheck/eingabe',
    values: {
      name: values.name,
      magistratsvorlageId: values.magistratsvorlageId,
      zielSetId: values.zielSetId
    },
    detail: {
      success: 'Mobilitätscheck erfolgreich erstellt',
      error: 'Fehler beim Erstellen des Mobilitätschecks'
    }
  })

  router.replace({
    name: 'mobilitaetscheck-ziele-neu',
    params: { id: route.params.id, checkId: response.id }
  })
  isSubmitting.value = false
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
