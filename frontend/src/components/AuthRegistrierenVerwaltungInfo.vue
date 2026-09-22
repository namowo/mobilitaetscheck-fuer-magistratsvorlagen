<template>
  <div class="grid grid-cols-1 gap-y-4 mt-4">
    <Message v-if="kommuneNichtDabei && kontaktEmail" severity="info" class="text-left">
      Ihre Kommune ist noch nicht Teil des Mobilitätschecks. Bitte senden Sie uns eine Nachricht. Wir stehen Ihnen beratend bei Einführung des Mobichecks zur Seite.
    </Message>

    <Message v-else-if="gemeindeId" severity="info" class="text-left">
      Für die Verwaltung erfolgt die Registrierung ausschließlich per Einladung. Ein Kollege von Ihnen ist für die Administration der Accounts in ihrer Kommune zuständig. Bitte fragen Sie diese Person nach einer Einladung.
    </Message>

    <div class="flex justify-between">
      <Button label="Zurück" severity="secondary" icon="pi pi-arrow-left" @click="$emit('zurueck')" />
      <Button
        v-if="kommuneNichtDabei && kontaktEmail"
        as="a"
        :href="mailtoHref"
        label="Nachricht senden"
        icon="pi pi-envelope"
      />
    </div>
  </div>
</template>

<script setup>
import { onMounted } from 'vue'
import Button from 'openvue/button'
import Message from 'openvue/message'
import { useKommuneAnfrageMailto } from '@/composables/kommuneAnfrageMailto'

defineProps({
  gemeindeId: { type: [Number, String], default: null },
  kommuneNichtDabei: { type: Boolean, default: false }
})
defineEmits(['zurueck'])

const { kontaktEmail, mailtoHref, fetchVorlage } = useKommuneAnfrageMailto('verwaltung')

onMounted(fetchVorlage)
</script>
