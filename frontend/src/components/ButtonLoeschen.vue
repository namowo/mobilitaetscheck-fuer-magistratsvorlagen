<template>
  <Button
    icon="pi pi-trash"
    @click="confirmDelete"
    size="small"
    severity="danger"
    :label="label"
    :disabled="props.disabled"
  />
</template>

<script setup>
import { computed } from 'vue'
import Button from 'openvue/button'
import { useConfirm } from 'openvue/useconfirm'

const props = defineProps({
  noLabel: {
    type: Boolean,
    default: false
  },
  disabled: {
    type: Boolean,
    default: false
  }
})

const label = computed(() => (props.noLabel ? '' : 'löschen'))

const emit = defineEmits(['delete-confirmed'])

const confirm = useConfirm()

const confirmDelete = () => {
  confirm.require({
    message: 'Möchtest du den Eintrag wirklich löschen?',
    header: 'Löschen bestätigen',
    icon: 'pi pi-exclamation-triangle',
    rejectProps: { label: 'Abbrechen', severity: 'secondary', outlined: true },
    acceptProps: { label: 'Löschen', severity: 'danger' },
    accept: () => emit('delete-confirmed')
  })
}
</script>
