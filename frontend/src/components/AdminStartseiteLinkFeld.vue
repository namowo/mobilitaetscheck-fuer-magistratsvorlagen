<template>
  <div class="grid gap-3 sm:grid-cols-2">
    <AdminStartseiteFeld label="Beschriftung" :feldId="`${idPrefix}-label`">
      <InputText :id="`${idPrefix}-label`" v-model="link.label" placeholder="z. B. Mehr erfahren" />
    </AdminStartseiteFeld>
    <AdminStartseiteFeld label="Ziel" :feldId="`${idPrefix}-ziel`">
      <Select
        :inputId="`${idPrefix}-ziel`"
        v-model="link.ziel"
        :options="LINK_ZIELE"
        optionLabel="label"
        optionValue="value"
      />
    </AdminStartseiteFeld>
    <AdminStartseiteFeld
      v-if="link.ziel === 'extern'"
      class="sm:col-span-2"
      label="Adresse"
      :feldId="`${idPrefix}-url`"
      hinweis="Externe Adressen (https://…) öffnen in einem neuen Tab; interne Pfade beginnen mit „/“."
    >
      <InputText
        :id="`${idPrefix}-url`"
        v-model="link.url"
        placeholder="https://www.beispiel.de oder /impressum"
        :invalid="!!link.url && !urlGueltig"
      />
    </AdminStartseiteFeld>
    <AdminStartseiteFeld v-if="mitStil" class="sm:col-span-2" label="Darstellung">
      <SelectButton
        v-model="link.stil"
        :options="BUTTON_STILE"
        optionLabel="label"
        optionValue="value"
        :allowEmpty="false"
      />
    </AdminStartseiteFeld>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import InputText from 'openvue/inputtext'
import Select from 'openvue/select'
import SelectButton from 'openvue/selectbutton'
import { BUTTON_STILE, LINK_ZIELE, neueId } from '@/utils/startseite'
import AdminStartseiteFeld from './AdminStartseiteFeld.vue'

const link = defineModel({ type: Object, required: true })
defineProps({ mitStil: { type: Boolean, default: true } })

const idPrefix = `link-${neueId()}`

const urlGueltig = computed(() => {
  const url = link.value.url?.trim() || ''
  return url.startsWith('/') || /^https?:\/\/[^\s]+\.[^\s]+/.test(url) || /^mailto:/.test(url)
})
</script>
