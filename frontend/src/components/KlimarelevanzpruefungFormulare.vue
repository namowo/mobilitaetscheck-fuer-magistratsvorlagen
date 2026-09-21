<template>
  <div>
    <Dialog
      v-model:visible="visibleF1"
      position="top"
      modal
      header="Fragebogen A"
      :style="{ width: '50rem' }"
    >
      <KlimarelevanzpruefungFormularEingabeFb1
        :key="openKeyF1"
        ref="fb1Ref"
        :editMode="!!klimarelevanzpruefung.fb1Id"
        :item="klimarelevanzpruefung.fb1"
        @add-item="onSubmit"
        @update-item="onUpdate"
      />
    </Dialog>
    <Dialog
      v-model:visible="visibleF2"
      position="top"
      modal
      header="Fragebogen B"
      :style="{ width: '50rem' }"
    >
      <KlimarelevanzpruefungFormularEingabeFb2
        :key="openKeyF2"
        ref="fb2Ref"
        :editMode="!!klimarelevanzpruefung.fb2Id"
        :item="klimarelevanzpruefung.fb2"
        @add-item="onSubmit"
        @update-item="onUpdate"
      />
    </Dialog>
    <Dialog
      v-model:visible="visibleF3"
      position="top"
      modal
      header="Fragebogen C"
      :style="{ width: '50rem' }"
    >
      <KlimarelevanzpruefungFormularEingabeFb3
        :key="openKeyF3"
        ref="fb3Ref"
        :editMode="!!klimarelevanzpruefung.fb3Id"
        :item="klimarelevanzpruefung.fb3"
        @add-item="onSubmit"
        @update-item="onUpdate"
      />
    </Dialog>
    <Dialog
      v-model:visible="visibleF4"
      position="top"
      modal
      header="Fragebogen D"
      :style="{ width: '50rem' }"
    >
      <KlimarelevanzpruefungFormularEingabeFb4
        :key="openKeyF4"
        ref="fb4Ref"
        :editMode="!!klimarelevanzpruefung.fb4Id"
        :item="klimarelevanzpruefung.fb4"
        @add-item="onSubmit"
        @update-item="onUpdate"
      />
    </Dialog>

    <div class="flex justify-end mb-4">
      <Button
        v-if="!isEditing"
        icon="pi pi-pencil"
        label="Fragen bearbeiten"
        severity="secondary"
        size="small"
        @click="onStartEditing"
      />
    </div>

    <form v-if="isEditing" @submit.prevent="onUpdateEingabe" class="mb-6">
      <div class="mb-8">
        <FloatLabel variant="on">
          <InputText id="edit-name" v-model="editName" class="w-full" inputClass="w-full" />
          <label for="edit-name">Name des Klimachecks</label>
        </FloatLabel>
      </div>
      <ol class="grid grid-cols-[11fr_1fr] gap-2 items-center list-outside list-decimal ms-6">
        <li @click="editF1 = !editF1">
          Es handelt sich um eine <strong>physische Maßnahme oder eine Beschaffung </strong> oder um
          die <strong>konkrete Planung/Konzept derer</strong>.<br />
          <small
            >(z.B. Begrünung, Abriss, Umbau, Installation, Anschaffung von Maschinen, Abholzungen /
            Fällungen, Flächennutzungsänderungen, Baumaßnahmen etc.)</small
          >
        </li>
        <ToggleSwitch v-model="editF1" :disabled="editDisableF1to4" />
        <Divider class="col-span-2" />
        <li @click="editF2 = !editF2">
          Es handelt sich um eine Planung / ein Konzept , das<strong>
            indirekt physische Maßnahmen nach sich zieht.</strong
          ><br /><small> (z.B. Bebauungsplan)</small>
        </li>
        <ToggleSwitch v-model="editF2" :disabled="editDisableF1to4" />
        <Divider class="col-span-2" />
        <li @click="editF3 = !editF3">
          Es handelt sich um eine Planung, ein Konzept, oder ein Vorhaben, die
          <strong
            >das Verhalten der Bevölkerung oder der kommunalen Mitarbeitenden in Bezug auf
            Klimaaspekte beeinflusst.</strong
          ><br />
          <small> (z.B. Klima-Bildungskampagne, Mobilitätsverhalten)</small>
        </li>
        <ToggleSwitch v-model="editF3" :disabled="editDisableF1to4" />
        <Divider class="col-span-2" />
        <li @click="editF4 = !editF4">
          Es handelt sich um ein Vorhaben, das
          <strong>nicht in eine der bisherigen Kategorien passt</strong>, aber dennoch klimawirksam
          ist.<br />
          <small>(z.B. Reisen)</small>
        </li>
        <ToggleSwitch v-model="editF4" :disabled="editDisableF1to4" />
        <Divider class="col-span-2" />
        <li @click="editF5 = !editF5">
          Es handelt sich um eine Maßnahme, die
          <strong>in keiner Weise klimawirksam</strong> ist.<br />
          <small
            >(z.B. Personaleinstellung, Mitgliedschaft außerhalb von Klimaschutz- /Klimaanpassung,
            Beantwortung von Anfragen, Wahlen etc.)</small
          >
        </li>
        <ToggleSwitch v-model="editF5" :disabled="editDisableF5" />
      </ol>
      <div class="flex justify-end gap-2 mt-6">
        <Button label="Abbrechen" severity="secondary" type="button" @click="isEditing = false" />
        <Button label="Speichern" type="submit" />
      </div>
    </form>

    <ol v-else class="grid grid-cols-[9fr_3fr] gap-2 items-center list-outside list-decimal ms-6">
      <li>
        Es handelt sich um eine <strong>physische Maßnahme oder eine Beschaffung </strong> oder um
        die <strong>konkrete Planung/Konzept derer</strong>.<br />
        <small
          >(z.B. Begrünung, Abriss, Umbau, Installation, Anschaffung von Maschinen, Abholzungen /
          Fällungen, Flächennutzungsänderungen, Baumaßnahmen etc.)</small
        >
      </li>
      <Button
        label="zum Fragebogen"
        @click="visibleF1 = true"
        :disabled="!klimarelevanzpruefung.f1"
        :severity="
          klimarelevanzpruefung.fb1Id
            ? klimarelevanzpruefung.fb1?.fertig
              ? 'success'
              : 'warn'
            : undefined
        "
      />
      <Divider class="col-span-2" />
      <li>
        Es handelt sich um eine Planung / ein Konzept , das<strong>
          indirekt physische Maßnahmen nach sich zieht.</strong
        ><br /><small> (z.B. Bebauungsplan)</small>
      </li>
      <Button
        label="zum Fragebogen"
        @click="visibleF2 = true"
        :disabled="!klimarelevanzpruefung.f2"
        :severity="
          klimarelevanzpruefung.fb2Id
            ? klimarelevanzpruefung.fb2?.fertig
              ? 'success'
              : 'warn'
            : undefined
        "
      />
      <Divider class="col-span-2" />
      <li>
        Es handelt sich um eine Planung, ein Konzept, oder ein Vorhaben, die
        <strong
          >das Verhalten der Bevölkerung oder der kommunalen Mitarbeitenden in Bezug auf
          Klimaaspekte beeinflusst.</strong
        ><br />
        <small> (z.B. Klima-Bildungskampagne, Mobilitätsverhalten)</small>
      </li>
      <Button
        label="zum Fragebogen"
        @click="visibleF3 = true"
        :disabled="!klimarelevanzpruefung.f3"
        :severity="
          klimarelevanzpruefung.fb3Id
            ? klimarelevanzpruefung.fb3?.fertig
              ? 'success'
              : 'warn'
            : undefined
        "
      />
      <Divider class="col-span-2" />
      <li>
        Es handelt sich um ein Vorhaben, das
        <strong>nicht in eine der bisherigen Kategorien passt</strong>, aber dennoch klimawirksam
        ist.<br />
        <small>(z.B. Reisen)</small>
      </li>
      <Button
        label="zum Fragebogen"
        @click="visibleF4 = true"
        :disabled="!klimarelevanzpruefung.f4"
        :severity="
          klimarelevanzpruefung.fb4Id
            ? klimarelevanzpruefung.fb4?.fertig
              ? 'success'
              : 'warn'
            : undefined
        "
      />
      <Divider class="col-span-2" />
      <li>
        Es handelt sich um eine Maßnahme, die <strong>in keiner Weise klimawirksam</strong> ist.
        <br />
        <small>
          (z.B. Personaleinstellung, Mitgliedschaft außerhalb von Klimaschutz- /Klimaanpassung,
          Beantwortung von Anfragen, Wahlen etc.)</small
        >
      </li>
      <Button label="Kein Fragebogen" :disabled="true" />
    </ol>

    <div class="mt-20 flex justify-end">
      <Button
        icon="pi pi-download"
        @click="onExport(route.params.klimarelevanzpruefungId)"
        label="PDF-Export"
        size="small"
        :disabled="!canExport"
        v-tooltip="!canExport ? 'Bitte alle Fragebögen vollständig ausfüllen' : undefined"
      />
    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { createItem, exportItem, fetchItem, updateItem, updateItemSilent } from '@/composables/crud'
import Button from 'openvue/button'
import Dialog from 'openvue/dialog'
import Divider from 'openvue/divider'
import FloatLabel from 'openvue/floatlabel'
import InputText from 'openvue/inputtext'
import ToggleSwitch from 'openvue/toggleswitch'
import KlimarelevanzpruefungFormularEingabeFb1 from './KlimarelevanzpruefungFormularEingabeFb1.vue'
import KlimarelevanzpruefungFormularEingabeFb2 from './KlimarelevanzpruefungFormularEingabeFb2.vue'
import KlimarelevanzpruefungFormularEingabeFb3 from './KlimarelevanzpruefungFormularEingabeFb3.vue'
import KlimarelevanzpruefungFormularEingabeFb4 from './KlimarelevanzpruefungFormularEingabeFb4.vue'

const route = useRoute()

const isLoading = ref(false)
const isEditing = ref(false)
const klimarelevanzpruefung = ref({ f1: false, f2: false, f3: false, f4: false, f5: false })
const visibleF1 = ref(false)
const visibleF2 = ref(false)
const visibleF3 = ref(false)
const visibleF4 = ref(false)

const fb1Ref = ref(null)
const fb2Ref = ref(null)
const fb3Ref = ref(null)
const fb4Ref = ref(null)

const openKeyF1 = ref(0)
const openKeyF2 = ref(0)
const openKeyF3 = ref(0)
const openKeyF4 = ref(0)

const canExport = computed(() => {
  const checks = [
    { id: klimarelevanzpruefung.value.fb1Id, fb: klimarelevanzpruefung.value.fb1 },
    { id: klimarelevanzpruefung.value.fb2Id, fb: klimarelevanzpruefung.value.fb2 },
    { id: klimarelevanzpruefung.value.fb3Id, fb: klimarelevanzpruefung.value.fb3 },
    { id: klimarelevanzpruefung.value.fb4Id, fb: klimarelevanzpruefung.value.fb4 }
  ]
  return checks.every(({ id, fb }) => !id || fb?.fertig === true)
})

const handleDialogClose = async (fbNumber, fbRef) => {
  const newItem = await fbRef.value?.triggerDraftSave()
  if (newItem) {
    klimarelevanzpruefung.value[`fb${fbNumber}Id`] = newItem.id
    klimarelevanzpruefung.value[`fb${fbNumber}`] = newItem
    await updateItemSilent({
      model: 'klimarelevanzpruefung/eingabe',
      modelId: route.params.klimarelevanzpruefungId,
      values: { [`fb${fbNumber}Id`]: newItem.id }
    })
  }
}

watch(visibleF1, (newVal, oldVal) => {
  if (newVal === true) openKeyF1.value++
  if (oldVal === true && newVal === false) handleDialogClose(1, fb1Ref)
})
watch(visibleF2, (newVal, oldVal) => {
  if (newVal === true) openKeyF2.value++
  if (oldVal === true && newVal === false) handleDialogClose(2, fb2Ref)
})
watch(visibleF3, (newVal, oldVal) => {
  if (newVal === true) openKeyF3.value++
  if (oldVal === true && newVal === false) handleDialogClose(3, fb3Ref)
})
watch(visibleF4, (newVal, oldVal) => {
  if (newVal === true) openKeyF4.value++
  if (oldVal === true && newVal === false) handleDialogClose(4, fb4Ref)
})

const editName = ref('')
const editF1 = ref(false)
const editF2 = ref(false)
const editF3 = ref(false)
const editF4 = ref(false)
const editF5 = ref(false)

const editDisableF1to4 = computed(() => editF5.value === true)
const editDisableF5 = computed(
  () =>
    editF1.value === true || editF2.value === true || editF3.value === true || editF4.value === true
)

watch(editF5, (newVal) => {
  if (newVal === true) {
    editF1.value = false
    editF2.value = false
    editF3.value = false
    editF4.value = false
  }
})

watch([editF1, editF2, editF3, editF4], ([val1, val2, val3, val4]) => {
  if (val1 || val2 || val3 || val4) {
    editF5.value = false
  }
})

const onStartEditing = () => {
  editName.value = klimarelevanzpruefung.value.name ?? ''
  editF1.value = klimarelevanzpruefung.value.f1 ?? false
  editF2.value = klimarelevanzpruefung.value.f2 ?? false
  editF3.value = klimarelevanzpruefung.value.f3 ?? false
  editF4.value = klimarelevanzpruefung.value.f4 ?? false
  editF5.value = klimarelevanzpruefung.value.f5 ?? false
  isEditing.value = true
}

const onUpdateEingabe = async () => {
  await updateItem({
    model: 'klimarelevanzpruefung/eingabe',
    modelId: route.params.klimarelevanzpruefungId,
    values: {
      name: editName.value,
      f1: editF1.value,
      f2: editF2.value,
      f3: editF3.value,
      f4: editF4.value,
      f5: editF5.value
    },
    detail: {
      success: 'Ausgangsfragen erfolgreich aktualisiert',
      error: 'Fehler beim Aktualisieren der Ausgangsfragen'
    }
  })
  klimarelevanzpruefung.value.name = editName.value
  klimarelevanzpruefung.value.f1 = editF1.value
  klimarelevanzpruefung.value.f2 = editF2.value
  klimarelevanzpruefung.value.f3 = editF3.value
  klimarelevanzpruefung.value.f4 = editF4.value
  klimarelevanzpruefung.value.f5 = editF5.value
  isEditing.value = false
}

const closeDialogs = () => {
  visibleF1.value = false
  visibleF2.value = false
  visibleF3.value = false
  visibleF4.value = false
}

onMounted(async () => {
  isLoading.value = true
  await fetchData()
  isLoading.value = false
})

const fetchData = async () => {
  klimarelevanzpruefung.value = await fetchItem(
    `/klimarelevanzpruefung/eingabe/${route.params.klimarelevanzpruefungId}`
  )
}

const onSubmit = async ({ fb, values }) => {
  const response = await createItem({
    model: `klimarelevanzpruefung/eingabe/fb${fb}`,
    values,
    detail: {
      success: `Fragebogen erfolgreich hinzugefügt`,
      error: `Fehler beim Hinzufügen des Fragebogens`
    }
  })
  await updateItemSilent({
    model: 'klimarelevanzpruefung/eingabe',
    modelId: route.params.klimarelevanzpruefungId,
    values: {
      [`f${fb}`]: true,
      [`fb${fb}Id`]: response.id
    }
  })
  klimarelevanzpruefung.value[`f${fb}`] = true
  klimarelevanzpruefung.value[`fb${fb}Id`] = response.id
  klimarelevanzpruefung.value[`fb${fb}`] = response
  closeDialogs()
}

const onUpdate = async ({ fb, modelId, values }) => {
  const response = await updateItem({
    model: `klimarelevanzpruefung/eingabe/fb${fb}`,
    modelId,
    values,
    detail: {
      success: `Fragebogen erfolgreich aktualisiert`,
      error: `Fehler beim Aktualisieren des Fragebogens`
    }
  })
  klimarelevanzpruefung.value[`fb${fb}`] = response
  closeDialogs()
}

const onExport = async (modelId) => {
  await exportItem({
    model: 'klimarelevanzpruefung',
    modelId,
    detail: {
      success: 'Klimarelevanzpruefung erfolgreich exportiert',
      error: 'Fehler beim Exportieren des Mobilitätschecks'
    }
  })
}
</script>

<style></style>
