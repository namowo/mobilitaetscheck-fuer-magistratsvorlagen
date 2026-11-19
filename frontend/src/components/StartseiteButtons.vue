<template>
  <div v-if="gueltigeLinks.length" class="flex flex-wrap gap-3" :class="zentriert ? 'justify-center' : ''">
    <template v-for="(link, index) in gueltigeLinks" :key="index">
      <!-- Admin preview: render inert buttons so unsaved edits aren't lost by navigating -->
      <Button
        v-if="vorschau"
        v-bind="buttonProps(link)"
        @click.prevent
      />

      <router-link v-else-if="ziel(link).to" :to="ziel(link).to" custom v-slot="{ navigate, href }">
        <span
          v-tooltip.top="
            istDeaktiviert(link) ? 'Es wurden noch keine Magistratsvorlagen veröffentlicht.' : undefined
          "
        >
          <Button
            v-bind="buttonProps(link)"
            as="a"
            :href="istDeaktiviert(link) ? undefined : href"
            :disabled="istDeaktiviert(link)"
            @click="!istDeaktiviert(link) && navigate($event)"
          />
        </span>
      </router-link>

      <Button
        v-else
        v-bind="buttonProps(link)"
        as="a"
        :href="ziel(link).href"
        target="_blank"
        rel="noopener noreferrer"
      />
    </template>
  </div>
</template>

<script setup>
import { computed, inject } from 'vue'
import Button from 'openvue/button'

const props = defineProps({
  links: { type: Array, default: () => [] },
  // Rendered on a dark background (accent colour or image)
  invertiert: { type: Boolean, default: false },
  zentriert: { type: Boolean, default: false },
  groesse: { type: String, default: 'large' }
})

const { kennzahlen, vorschau } = inject('startseite', { kennzahlen: null, vorschau: false })

const ziel = (link) => {
  if (link.ziel !== 'extern') return { to: { name: link.ziel } }
  const url = (link.url || '').trim()
  return url.startsWith('/') ? { to: url } : { href: url }
}

const gueltigeLinks = computed(() =>
  props.links.filter((l) => l?.label?.trim() && (l.ziel !== 'extern' || l.url?.trim()))
)

const istDeaktiviert = (link) =>
  link.ziel === 'oeffentlich-magistratsvorlagen' && kennzahlen?.value?.magistratsvorlagen === 0

const buttonProps = (link) => {
  const primaer = link.stil !== 'sekundaer'
  const istExtern = link.ziel === 'extern' && !link.url?.trim().startsWith('/')
  return {
    label: link.label,
    size: props.groesse,
    icon: istExtern ? 'pi pi-external-link' : primaer ? 'pi pi-arrow-right' : undefined,
    iconPos: 'right',
    outlined: !primaer && !props.invertiert,
    class: props.invertiert ? (primaer ? 'startseite-btn-hell' : 'startseite-btn-umriss-hell') : ''
  }
}
</script>
