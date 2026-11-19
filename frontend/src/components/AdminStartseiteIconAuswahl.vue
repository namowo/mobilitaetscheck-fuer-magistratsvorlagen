<template>
  <Select
    v-model="icon"
    :inputId="inputId"
    :options="OPTIONEN"
    optionLabel="label"
    optionValue="value"
    filter
    showClear
    placeholder="Kein Icon"
  >
    <template #value="{ value, placeholder }">
      <span v-if="value" class="flex items-center gap-2"><i :class="value" />{{ name(value) }}</span>
      <span v-else>{{ placeholder }}</span>
    </template>
    <template #option="{ option }">
      <span class="flex items-center gap-2"><i :class="option.value" />{{ option.label }}</span>
    </template>
  </Select>
</template>

<script setup>
import Select from 'openvue/select'
import { ICONS } from '@/utils/startseite'

const icon = defineModel({ type: String, default: '' })
defineProps({ inputId: { type: String, default: undefined } })

const name = (wert) => wert.replace('pi pi-', '')
const OPTIONEN = ICONS.map((value) => ({ value, label: name(value) }))
</script>
