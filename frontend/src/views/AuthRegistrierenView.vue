<template>
  <div class="flex items-start justify-center pt-12 px-4">
    <div class="w-full max-w-lg">
      <BaseCard class="p-2">
        <div class="text-center mb-8">
          <AuthLogoLeiste />
          <h1 class="text-xl font-bold text-gray-800">Registrieren</h1>
          <p class="text-sm text-gray-500">
            {{
              token
                ? 'Sie wurden eingeladen, einen Account zu erstellen.'
                : 'In drei Schritten zur Registrierung.'
            }}
          </p>
        </div>
        <AuthRegistrierenEinladungFormular v-if="token" />
        <Stepper v-else v-model:value="step" linear>
          <StepList>
            <Step value="1" />
            <Step value="2" />
            <Step value="3" />
          </StepList>
          <StepPanels>
            <StepPanel v-slot="{ activateCallback }" value="1">
              <p class="text-sm text-gray-500 mt-4">
                Wählen Sie aus, ob Sie für die Politik oder die Verwaltung tätig sind.
              </p>
              <div class="field mt-4">
                <FloatLabel variant="on">
                  <Select
                    id="rolle"
                    v-model="rolle"
                    :options="rolleOptionen"
                    optionLabel="label"
                    optionValue="value"
                    class="w-full"
                  />
                  <label for="rolle">Rolle</label>
                </FloatLabel>
              </div>
              <div class="flex pt-6 justify-end">
                <Button
                  label="Weiter"
                  icon="pi pi-arrow-right"
                  iconPos="right"
                  :disabled="!rolle"
                  @click="activateCallback('2')"
                />
              </div>
            </StepPanel>

            <StepPanel v-slot="{ activateCallback }" value="2">
              <BaseSpinner v-if="isLoadingGemeinden" />
              <template v-else>
                <p class="text-sm text-gray-500 mt-4">
                  Wählen Sie Ihre Kommune aus. Ist Ihre Kommune nicht gelistet, dann wählen Sie "Meine Kommune ist nicht dabei".
                </p>
                <div class="field mt-4">
                  <FloatLabel variant="on">
                    <Select
                      id="gemeinde"
                      v-model="gemeindeId"
                      :options="gemeindeOptionenMitHinweis"
                      optionLabel="name"
                      optionValue="id"
                      class="w-full"
                    />
                    <label for="gemeinde">Kommune</label>
                  </FloatLabel>
                </div>
                <div class="flex pt-6 justify-between">
                  <Button
                    label="Zurück"
                    severity="secondary"
                    icon="pi pi-arrow-left"
                    @click="activateCallback('1')"
                  />
                  <Button
                    label="Weiter"
                    icon="pi pi-arrow-right"
                    iconPos="right"
                    :disabled="!gemeindeId"
                    @click="activateCallback('3')"
                  />
                </div>
              </template>
            </StepPanel>

            <StepPanel v-slot="{ activateCallback }" value="3">
              <p
                v-if="rolle === 'politik' && gemeindeId !== KOMMUNE_NICHT_DABEI"
                class="text-sm text-gray-500 mt-4"
              >
                Geben Sie Ihre Daten ein, um die Registrierung abzuschließen.
              </p>
              <p v-else-if="rolle === 'verwaltung'" class="text-sm text-gray-500 mt-4">
                So geht es für die Verwaltung weiter.
              </p>
              <AuthRegistrierenPolitikFormular
                v-if="rolle === 'politik'"
                :gemeinde-id="gemeindeId"
                :kommune-nicht-dabei="gemeindeId === KOMMUNE_NICHT_DABEI"
                @zurueck="activateCallback('2')"
              />
              <AuthRegistrierenVerwaltungInfo
                v-else-if="rolle === 'verwaltung'"
                :gemeinde-id="gemeindeId"
                :kommune-nicht-dabei="gemeindeId === KOMMUNE_NICHT_DABEI"
                @zurueck="activateCallback('2')"
              />
            </StepPanel>
          </StepPanels>
        </Stepper>
        <div class="border-t border-gray-100 mt-6 pt-4 text-sm">
          <RouterLink class="text-blue-600 hover:underline" :to="{ name: 'anmelden' }">
            Bereits registriert? Hier anmelden
          </RouterLink>
        </div>
      </BaseCard>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import { useRoute } from 'vue-router'
import AuthRegistrierenPolitikFormular from '@/components/AuthRegistrierenPolitikFormular.vue'
import AuthRegistrierenVerwaltungInfo from '@/components/AuthRegistrierenVerwaltungInfo.vue'
import AuthRegistrierenEinladungFormular from '@/components/AuthRegistrierenEinladungFormular.vue'
import Stepper from 'openvue/stepper'
import StepList from 'openvue/steplist'
import StepPanels from 'openvue/steppanels'
import Step from 'openvue/step'
import StepPanel from 'openvue/steppanel'
import Select from 'openvue/select'
import FloatLabel from 'openvue/floatlabel'
import Button from 'openvue/button'
import AuthLogoLeiste from '@/components/AuthLogoLeiste.vue'
import { apiClient } from '@/services/axios'

const KOMMUNE_NICHT_DABEI = 'nicht-dabei'

const route = useRoute()
const token = route.query.token

const rolleOptionen = [
  { label: 'Politik', value: 'politik' },
  { label: 'Verwaltung', value: 'verwaltung' }
]
const rolle = ref(null)
const step = ref('1')

const isLoadingGemeinden = ref(false)
const gemeindeOptions = ref([])
const gemeindeId = ref(null)

const gemeindeOptionenMitHinweis = computed(() => [
  { id: KOMMUNE_NICHT_DABEI, name: 'Meine Kommune ist nicht dabei' },
  ...gemeindeOptions.value
])

watch(rolle, () => {
  gemeindeId.value = null
})

onMounted(async () => {
  isLoadingGemeinden.value = true
  try {
    const res = await apiClient.get('/option/gemeinde')
    gemeindeOptions.value = res.data
  } catch {
    gemeindeOptions.value = []
  } finally {
    isLoadingGemeinden.value = false
  }
})
</script>
