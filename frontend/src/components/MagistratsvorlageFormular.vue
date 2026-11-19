<template>
  <div>
    <!-- Bestehende Vorlage: Überschrift mit Bearbeiten/Abbrechen -->
    <div v-if="editMode" class="flex items-center justify-between gap-4">
      <BaseSubheading>Allgemeine Daten</BaseSubheading>
      <Skeleton v-if="!istGeladen && !isPolitik" width="7rem" height="2rem" />
      <template v-else-if="!isPolitik">
        <ButtonBearbeiten v-if="!isEditing" @click="isEditing = true" />
        <Button
          v-else
          icon="pi pi-times"
          label="abbrechen"
          size="small"
          severity="secondary"
          outlined
          @click="cancelEdit"
        />
      </template>
    </div>

    <!-- Platzhalter in der Form des Inhalts, damit beim Laden nichts springt -->
    <template v-if="!istGeladen">
      <div
        v-if="editMode"
        class="my-4 rounded-lg border border-gray-200 bg-white shadow-sm overflow-hidden"
      >
        <dl class="divide-y divide-gray-100 text-sm">
          <div class="grid gap-1 px-5 py-3 sm:grid-cols-[14rem_1fr] sm:gap-4">
            <dt class="text-gray-500">Magistratsvorlagennummer</dt>
            <dd><Skeleton width="8rem" height="1.25rem" /></dd>
          </div>
          <div class="grid gap-1 px-5 py-3 sm:grid-cols-[14rem_1fr] sm:gap-4">
            <dt class="text-gray-500">Datum der Magistratssitzung</dt>
            <dd><Skeleton width="6rem" height="1.25rem" /></dd>
          </div>
          <div class="grid gap-1 px-5 py-3 sm:grid-cols-[14rem_1fr] sm:gap-4">
            <dt class="text-gray-500">Gebiete</dt>
            <dd><Skeleton width="12rem" height="1.25rem" /></dd>
          </div>
          <div class="grid gap-1 px-5 py-3 sm:grid-cols-[14rem_1fr] sm:gap-4">
            <dt class="text-gray-500">Tags</dt>
            <dd><Skeleton width="10rem" height="1.25rem" /></dd>
          </div>
          <div class="grid gap-1 px-5 py-3 sm:grid-cols-[14rem_1fr] sm:gap-4">
            <dt class="text-gray-500">Beschreibung der Maßnahme</dt>
            <dd><Skeleton width="70%" height="1.25rem" /></dd>
          </div>
        </dl>
      </div>
      <div v-else class="grid grid-cols-1 gap-y-4 my-7">
        <Skeleton v-for="i in 5" :key="i" height="3rem" class="w-full" />
        <Skeleton height="12rem" class="w-full" />
      </div>
    </template>

    <!-- Read-only view (Politik immer, Verwaltung bis "bearbeiten") -->
    <div
      v-else-if="showReadOnly"
      class="my-4 rounded-lg border border-gray-200 bg-white shadow-sm overflow-hidden"
    >
      <dl class="divide-y divide-gray-100 text-sm">
        <div class="grid gap-1 px-5 py-3 sm:grid-cols-[14rem_1fr] sm:gap-4">
          <dt class="text-gray-500">Magistratsvorlagennummer</dt>
          <dd class="text-gray-900">{{ vorlage?.verwaltungsvorgangNr || '—' }}</dd>
        </div>
        <div class="grid gap-1 px-5 py-3 sm:grid-cols-[14rem_1fr] sm:gap-4">
          <dt class="text-gray-500">Datum der Magistratssitzung</dt>
          <dd class="text-gray-900">
            {{
              vorlage?.verwaltungsvorgangDatum
                ? new Date(vorlage.verwaltungsvorgangDatum).toLocaleDateString('de-DE')
                : '—'
            }}
          </dd>
        </div>
        <div class="grid gap-1 px-5 py-3 sm:grid-cols-[14rem_1fr] sm:gap-4">
          <dt class="text-gray-500">Gebiete</dt>
          <dd>
            <div v-if="vorlage?.gemeindeGebiete?.length" class="flex flex-wrap gap-1">
              <Tag
                v-for="gebiet in vorlage.gemeindeGebiete"
                :key="gebiet.id"
                :value="gebiet.name"
                severity="secondary"
              />
            </div>
            <span v-else class="text-gray-900">—</span>
          </dd>
        </div>
        <div class="grid gap-1 px-5 py-3 sm:grid-cols-[14rem_1fr] sm:gap-4">
          <dt class="text-gray-500">Tags</dt>
          <dd>
            <div v-if="vorlage?.tags?.length" class="flex flex-wrap gap-1">
              <Tag v-for="tag in vorlage.tags" :key="tag.id" :value="'#' + tag.name" severity="info" />
            </div>
            <span v-else class="text-gray-900">—</span>
          </dd>
        </div>
        <div class="grid gap-1 px-5 py-3 sm:grid-cols-[14rem_1fr] sm:gap-4">
          <dt class="text-gray-500">Beschreibung der Maßnahme</dt>
          <dd>
            <div
              v-if="vorlage?.beschreibung"
              class="prose prose-sm max-w-none text-gray-900"
              v-html="vorlage.beschreibung"
            ></div>
            <span v-else class="text-gray-900">—</span>
          </dd>
        </div>
      </dl>
    </div>

    <!-- Editable form for Verwaltung -->
    <form v-else class="grid grid-cols-1 gap-y-4 my-7" @submit.prevent="onSubmit">
      <div class="form-group field" data-tour="vorlage-formular-start">
        <FloatLabel variant="on">
          <InputText
            id="verwaltungsvorgangNr"
            v-model="verwaltungsvorgangNr"
            :invalid="!!errors.verwaltungsvorgangNr"
            class="w-full"
            inputClass="w-full"
          />
          <label for="verwaltungsvorgangNr">Magistratsvorlagennummer</label>
        </FloatLabel>
        <small
          v-if="errors.verwaltungsvorgangNr"
          id="verwaltungsvorgangNr-help"
          class="p-error block"
        >
          {{ errors.verwaltungsvorgangNr }}
        </small>
      </div>

      <div class="form-group field">
        <FloatLabel variant="on">
          <DatePicker
            id="verwaltungsvorgangDatum"
            v-model="verwaltungsvorgangDatum"
            showIcon
            iconDisplay="input"
            :invalid="!!errors.verwaltungsvorgangDatum"
            class="w-full sm:w-80"
            inputClass="w-full"
          />
          <label for="verwaltungsvorgangDatum">Datum der Magistratssitzung <LabelOptional /></label>
        </FloatLabel>
        <small
          v-if="errors.verwaltungsvorgangDatum"
          id="verwaltungsvorgangDatum-help"
          class="p-error block"
        >
          {{ errors.verwaltungsvorgangDatum }}
        </small>
      </div>

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
          <label for="name">Titel der Magistratsvorlage</label>
        </FloatLabel>
        <small v-if="errors.name" id="name-help" class="p-error block">{{ errors.name }}</small>
      </div>
      <div>
        <FloatLabel variant="on">
          <MultiSelect
            id="gemeindeGebietIds"
            v-model="gemeindeGebietIds"
            :options="gebiete"
            optionLabel="name"
            optionValue="id"
            display="chip"
            class="w-full"
            filter
            :disabled="keineGebiete"
            :invalid="!!errors.gemeindeGebietIds"
          />
          <label for="gemeindeGebietIds">Gebiete auswählen <LabelOptional /></label>
        </FloatLabel>
        <small v-if="keineGebiete" class="block mt-1 text-xs text-gray-500">
          Für Ihre Kommune sind noch keine Gebiete angelegt.
          <RouterLink :to="{ name: 'gemeinde-gebiet' }" class="underline hover:text-gray-700"
            >Gebiete anlegen</RouterLink
          >
        </small>
        <small v-if="errors.gemeindeGebietIds" id="gemeindeGebietIds-help" class="p-error block">{{
          errors.gemeindeGebietIds
        }}</small>
      </div>
      <div>
        <FloatLabel variant="on">
          <MultiSelect
            id="tagIds"
            v-model="tagIds"
            :options="tagOptions"
            optionLabel="name"
            optionValue="id"
            display="chip"
            class="w-full"
            filter
            :invalid="!!errors.tagIds"
          />
          <label for="tagIds">Tags auswählen <LabelOptional /></label>
        </FloatLabel>
        <small v-if="errors.gemeindeGebietIds" id="tagIds-help" class="p-error block">{{
          errors.tagIds
        }}</small>
      </div>
      <div class="form-group field">
        <label class="text-sm text-gray-500 mb-1 block">Beschreibung der Maßnahme <LabelOptional /></label>
        <Editor
          id="beschreibung"
          v-model="beschreibung"
          rows="5"
          :invalid="!!errors.beschreibung"
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
        <small v-if="errors.beschreibung" id="beschreibung-help" class="p-error block">{{
          errors.beschreibung
        }}</small>
      </div>
      <div class="flex justify-end w-full">
        <Button icon="pi pi-save" type="submit" label="speichern" :loading="isLoading" />
      </div>
      <div v-if="editMode">
        <Divider />
        <BaseSubheading>Danger Zone</BaseSubheading>
        <div class="mt-4">
          <Button
            @click="confirmDelete()"
            icon="pi pi-trash"
            label="Magistratsvorlage löschen"
            severity="danger"
          />
        </div>
      </div>
    </form>
  </div>
</template>

<script setup>
import { computed, inject, onActivated, onMounted, ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { useForm } from 'vee-validate'
import { schema } from '@/utils/schemas/magistratsvorlage'
import { toTypedSchema } from '@vee-validate/yup'
import { createItem, deleteItem, fetchItems, updateItem } from '@/composables/crud'
import { useConfirm } from 'openvue/useconfirm'
import Button from 'openvue/button'
import Divider from 'openvue/divider'
import InputText from 'openvue/inputtext'
import DatePicker from 'openvue/datepicker'
import Editor from 'openvue/editor'
import FloatLabel from 'openvue/floatlabel'
import MultiSelect from 'openvue/multiselect'
import Tag from 'openvue/tag'
import ButtonBearbeiten from '@/components/ButtonBearbeiten.vue'
import Skeleton from 'openvue/skeleton'

const confirm = useConfirm()
const authStore = useAuthStore()
const isPolitik = computed(() => authStore.effectiveRolleId === 2)

const props = defineProps({
  editMode: {
    type: Boolean,
    default: true
  }
})

const router = useRouter()
const route = useRoute()
const isLoading = ref(false)
const istGeladen = ref(false)
const gebiete = ref([])
const tagOptions = ref([])
const gebieteGeladen = ref(false)
const keineGebiete = computed(() => gebieteGeladen.value && gebiete.value.length === 0)
const vorlage = ref(null)
const ladeVorlageKopf = inject('ladeVorlage', null)
// Neue Vorlagen starten direkt im Formular, bestehende zuerst in der Leseansicht.
const isEditing = ref(!props.editMode)
const showReadOnly = computed(() => isPolitik.value || !isEditing.value)

const { defineField, handleSubmit, errors, setValues } = useForm({
  validationSchema: toTypedSchema(schema)
})

const [verwaltungsvorgangNr] = defineField('verwaltungsvorgangNr')
const [verwaltungsvorgangDatum] = defineField('verwaltungsvorgangDatum')
const [name] = defineField('name')
const [beschreibung] = defineField('beschreibung')
const [gemeindeGebietIds] = defineField('gemeindeGebietIds')
const [tagIds] = defineField('tagIds')

onMounted(async () => {
  await Promise.all([
    props.editMode ? fetchMagistratsvorlage() : null,
    !isPolitik.value ? fetchOptions() : null
  ])
  istGeladen.value = true
})

// Beim Zurückkehren in den Reiter still aktualisieren – aber nie laufende Bearbeitungen überschreiben.
let ersteAktivierung = true
onActivated(() => {
  if (ersteAktivierung) return (ersteAktivierung = false)
  if (props.editMode && !isEditing.value) fetchMagistratsvorlage()
})

const fetchOptions = async () => {
  const [gebieteResponse, tagsResponse] = await Promise.all([
    fetchItems('einstellungen/gebiet'),
    fetchItems('/einstellungen/tag')
  ])
  gebiete.value = gebieteResponse ?? []
  gebieteGeladen.value = true
  tagOptions.value = tagsResponse
}

// Kein Lade-Flag hier: nach dem Speichern wird still neu geladen, ohne Platzhalter.
const fetchMagistratsvorlage = async () => {
  const response = await fetchItems(`/magistratsvorlage/${route.params.id}`)
  vorlage.value = response
  setValuesFromVorlage(response)
}

const setValuesFromVorlage = (response) => {
  if (!response) return
  setValues({
    verwaltungsvorgangNr: response.verwaltungsvorgangNr,
    verwaltungsvorgangDatum: response.verwaltungsvorgangDatum ? new Date(response.verwaltungsvorgangDatum) : null,
    name: response.name,
    beschreibung: response.beschreibung,
    gemeindeId: response.gemeindeId,
    gemeindeGebietIds: response.gemeindeGebietIds,
    tagIds: response.tagIds
  })
}

const cancelEdit = () => {
  setValuesFromVorlage(vorlage.value)
  isEditing.value = false
}

const onSubmit = handleSubmit(async (values) => {
  if (props.editMode) {
    const response = await updateItem({
      model: 'magistratsvorlage',
      modelId: route.params.id,
      values: values,
      detail: {
        success: 'Magistratsvorlage erfolgreich aktualisiert',
        error: 'Fehler beim Aktualisieren der Magistratsvorlage'
      }
    })
    if (!response) return
    await Promise.all([fetchMagistratsvorlage(), ladeVorlageKopf?.()])
    isEditing.value = false
  } else {
    isLoading.value = true
    const response = await createItem({
      model: 'magistratsvorlage',
      values: values,
      detail: {
        success: 'Magistratsvorlage erfolgreich erstellt',
        error: 'Fehler beim Erstellen der Magistratsvorlage'
      }
    })

    isLoading.value = false
    if (!response) return

    router.replace({
      name: 'magistratsvorlage-id-daten',
      params: { id: response.id }
    })
  }
})

const confirmDelete = () => {
  confirm.require({
    message: 'Möchten Sie diese Magistratsvorlage löschen?',
    header: 'Löschen bestätigen',
    icon: 'pi pi-exclamation-triangle',
    rejectProps: {
      label: 'Abbrechen',
      severity: 'secondary',
      outlined: true
    },
    acceptProps: {
      label: 'löschen',
      severity: 'danger'
    },
    accept: async () => {
      await deleteItem({
        model: 'magistratsvorlage',
        modelId: route.params.id,
        detail: {
          success: 'Magistratsvorlage erfolgreich gelöscht.',
          error: 'Fehler beim Löschen der Magistratsvorlage.'
        }
      })
      router.push({ name: 'magistratsvorlage-liste' })
    }
  })
}
</script>

<style scoped>
.p-invalid {
  @apply border-red-600 text-red-600;
}

.p-error {
  @apply text-red-600;
}
</style>
