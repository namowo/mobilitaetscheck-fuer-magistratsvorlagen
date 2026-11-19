<template>
  <div class="max-w-3xl mx-auto">
    <StartseiteUeberschrift :titel="block.titel" />

    <Accordion :value="null" class="startseite-faq rounded-xl overflow-hidden border border-gray-200 bg-white text-gray-900">
      <AccordionPanel v-for="eintrag in fragen" :key="eintrag.id" :value="eintrag.id">
        <AccordionHeader>{{ eintrag.frage }}</AccordionHeader>
        <AccordionContent>
          <div class="rich-content" v-html="eintrag.antwort" />
        </AccordionContent>
      </AccordionPanel>
    </Accordion>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import Accordion from 'openvue/accordion'
import AccordionPanel from 'openvue/accordionpanel'
import AccordionHeader from 'openvue/accordionheader'
import AccordionContent from 'openvue/accordioncontent'
import StartseiteUeberschrift from './StartseiteUeberschrift.vue'

const props = defineProps({ block: { type: Object, required: true } })
const fragen = computed(() => (props.block.eintraege || []).filter((e) => e.frage?.trim()))
</script>

<style scoped>
.startseite-faq :deep(.p-accordionpanel:last-child) {
  border-bottom: 0;
}
.startseite-faq :deep(.p-accordionheader) {
  font-size: 1rem;
}
</style>
