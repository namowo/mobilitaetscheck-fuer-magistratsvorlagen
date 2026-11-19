<template>
  <div class="flex flex-col gap-2">
    <draggable
      :list="eintraege"
      item-key="id"
      handle=".listen-griff"
      class="flex flex-col gap-2"
    >
      <template #item="{ element, index }">
        <div class="border border-gray-200 rounded-md bg-gray-50/60">
          <div class="flex items-center gap-2 px-3 py-1.5 border-b border-gray-200">
            <i class="pi pi-bars listen-griff cursor-move text-gray-400" title="Ziehen zum Verschieben" />
            <span class="text-sm font-semibold text-gray-600 flex-1 truncate">
              {{ elementName }} {{ index + 1 }}<template v-if="titelVon(element)">: {{ titelVon(element) }}</template>
            </span>
            <Button
              icon="pi pi-arrow-up"
              text
              rounded
              size="small"
              severity="secondary"
              :disabled="index === 0"
              v-tooltip.top="'Nach oben'"
              :aria-label="`${elementName} nach oben`"
              @click="verschieben(index, -1)"
            />
            <Button
              icon="pi pi-arrow-down"
              text
              rounded
              size="small"
              severity="secondary"
              :disabled="index === eintraege.length - 1"
              v-tooltip.top="'Nach unten'"
              :aria-label="`${elementName} nach unten`"
              @click="verschieben(index, 1)"
            />
            <Button
              icon="pi pi-trash"
              text
              rounded
              size="small"
              severity="danger"
              :disabled="eintraege.length <= min"
              v-tooltip.top="'Entfernen'"
              :aria-label="`${elementName} entfernen`"
              @click="eintraege.splice(index, 1)"
            />
          </div>
          <div class="p-3 flex flex-col gap-3">
            <slot :eintrag="element" :index="index" />
          </div>
        </div>
      </template>
    </draggable>

    <div>
      <Button
        :label="`${elementName} hinzufügen`"
        icon="pi pi-plus"
        size="small"
        outlined
        :disabled="max !== null && eintraege.length >= max"
        @click="eintraege.push(neu())"
      />
    </div>
  </div>
</template>

<script setup>
import draggable from 'vuedraggable'
import Button from 'openvue/button'

const eintraege = defineModel({ type: Array, required: true })

defineProps({
  neu: { type: Function, required: true },
  elementName: { type: String, default: 'Eintrag' },
  titelVon: { type: Function, default: () => '' },
  min: { type: Number, default: 0 },
  max: { type: Number, default: null }
})

const verschieben = (index, richtung) => {
  const [element] = eintraege.value.splice(index, 1)
  eintraege.value.splice(index + richtung, 0, element)
}
</script>
