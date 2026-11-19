<template>
  <div class="flex flex-col gap-4">
    <!-- Hero -->
    <template v-if="block.typ === 'hero'">
      <AdminStartseiteFeld label="Titel" :feldId="id('titel')">
        <InputText :id="id('titel')" v-model="block.titel" />
      </AdminStartseiteFeld>
      <AdminStartseiteFeld label="Untertitel" optional :feldId="id('untertitel')">
        <Textarea :id="id('untertitel')" v-model="block.untertitel" autoResize rows="2" />
      </AdminStartseiteFeld>
      <AdminStartseiteFeld label="Bild" optional>
        <AdminStartseiteBildFeld v-model="block.bildUrl" />
      </AdminStartseiteFeld>
      <AdminStartseiteFeld
        v-if="block.bildUrl"
        label="Bildanordnung"
        hinweis="Bei „Hintergrund“ wird das Bild abgedunkelt und der Text weiß dargestellt."
      >
        <SelectButton
          v-model="block.layout"
          :options="HERO_LAYOUTS"
          optionLabel="label"
          optionValue="value"
          :allowEmpty="false"
        />
      </AdminStartseiteFeld>
      <AdminStartseiteFeld label="Buttons" optional>
        <AdminStartseiteListe
          v-model="block.buttons"
          :neu="() => neuerLink({ stil: block.buttons.length ? 'sekundaer' : 'primaer' })"
          elementName="Button"
          :titelVon="(l) => l.label"
          :max="3"
        >
          <template #default="{ index }">
            <AdminStartseiteLinkFeld v-model="block.buttons[index]" />
          </template>
        </AdminStartseiteListe>
      </AdminStartseiteFeld>
    </template>

    <!-- Text -->
    <template v-else-if="block.typ === 'text'">
      <AdminStartseiteFeld label="Überschrift" optional :feldId="id('titel')">
        <InputText :id="id('titel')" v-model="block.titel" />
      </AdminStartseiteFeld>
      <AdminStartseiteFeld label="Text">
        <RichContentEditor v-model="block.inhalt" />
      </AdminStartseiteFeld>
    </template>

    <!-- Video -->
    <template v-else-if="block.typ === 'video'">
      <AdminStartseiteFeld
        label="Video-Link"
        :feldId="id('url')"
        hinweis="Link aus der Adresszeile oder über „Teilen“ kopieren, z. B. https://www.youtube.com/watch?v=… oder https://vimeo.com/…"
      >
        <InputText
          :id="id('url')"
          v-model.trim="block.url"
          placeholder="https://www.youtube.com/watch?v=…"
          :invalid="!!block.url && !video"
        />
      </AdminStartseiteFeld>
      <Message v-if="video" severity="success" size="small" icon="pi pi-check">
        {{ VIDEO_ANBIETER[video.anbieter].name }}-Video erkannt. Es wird datenschutzfreundlich eingebettet
        und erst nach einem Klick der Besucherin bzw. des Besuchers geladen.
      </Message>
      <Message v-else-if="block.url" severity="error" size="small">
        Dieser Link wird nicht erkannt. Unterstützt werden YouTube- und Vimeo-Links.
      </Message>

      <div class="grid gap-4 sm:grid-cols-2">
        <AdminStartseiteFeld label="Überschrift" optional :feldId="id('titel')">
          <InputText :id="id('titel')" v-model="block.titel" />
        </AdminStartseiteFeld>
        <AdminStartseiteFeld label="Bildunterschrift" optional :feldId="id('unterschrift')">
          <InputText :id="id('unterschrift')" v-model="block.bildunterschrift" />
        </AdminStartseiteFeld>
      </div>
      <AdminStartseiteFeld label="Beschreibung" optional :feldId="id('text')">
        <Textarea :id="id('text')" v-model="block.text" autoResize rows="2" />
      </AdminStartseiteFeld>
      <AdminStartseiteFeld
        label="Vorschaubild"
        optional
        hinweis="Wird angezeigt, bevor das Video geladen wird. Das Vorschaubild des Anbieters wird aus Datenschutzgründen nicht automatisch abgerufen – ohne eigenes Bild erscheint eine Fläche in der Akzentfarbe."
      >
        <AdminStartseiteBildFeld v-model="block.vorschaubildUrl" />
      </AdminStartseiteFeld>
      <AdminStartseiteFeld label="Seitenverhältnis">
        <SelectButton
          v-model="block.seitenverhaeltnis"
          :options="SEITENVERHAELTNISSE"
          optionLabel="label"
          optionValue="value"
          :allowEmpty="false"
        />
      </AdminStartseiteFeld>

      <Message severity="info" size="small">
        <div class="flex flex-col gap-2">
          <span>
            Ergänzen Sie Ihre Datenschutzerklärung um einen Abschnitt zu eingebetteten Videos. Ein
            Textvorschlag kann kopiert und unter
            <router-link :to="{ name: 'admin-datenschutz' }" class="underline">Datenschutz</router-link>
            eingefügt werden – bitte rechtlich prüfen lassen.
          </span>
          <div>
            <Button
              label="Textvorschlag kopieren"
              icon="pi pi-copy"
              size="small"
              outlined
              @click="kopiereDatenschutzText"
            />
          </div>
        </div>
      </Message>
    </template>

    <!-- Kacheln -->
    <template v-else-if="block.typ === 'kacheln'">
      <div class="grid gap-4 sm:grid-cols-2">
        <AdminStartseiteFeld label="Überschrift" optional :feldId="id('titel')">
          <InputText :id="id('titel')" v-model="block.titel" />
        </AdminStartseiteFeld>
        <AdminStartseiteFeld label="Untertitel" optional :feldId="id('untertitel')">
          <InputText :id="id('untertitel')" v-model="block.untertitel" />
        </AdminStartseiteFeld>
      </div>
      <AdminStartseiteFeld label="Spalten (auf großen Bildschirmen)">
        <SelectButton v-model="block.spalten" :options="[2, 3, 4]" :allowEmpty="false" />
      </AdminStartseiteFeld>
      <AdminStartseiteListe
        v-model="block.kacheln"
        :neu="neueKachel"
        elementName="Kachel"
        :titelVon="(k) => k.titel"
        :max="12"
      >
        <template #default="{ eintrag }">
          <div class="grid gap-3 sm:grid-cols-[14rem_1fr]">
            <AdminStartseiteFeld label="Icon" optional :feldId="id(`icon-${eintrag.id}`)">
              <AdminStartseiteIconAuswahl v-model="eintrag.icon" :inputId="id(`icon-${eintrag.id}`)" />
            </AdminStartseiteFeld>
            <AdminStartseiteFeld label="Titel" :feldId="id(`titel-${eintrag.id}`)">
              <InputText :id="id(`titel-${eintrag.id}`)" v-model="eintrag.titel" />
            </AdminStartseiteFeld>
          </div>
          <AdminStartseiteFeld label="Text" optional :feldId="id(`text-${eintrag.id}`)">
            <Textarea :id="id(`text-${eintrag.id}`)" v-model="eintrag.text" autoResize rows="2" />
          </AdminStartseiteFeld>
          <div class="flex items-center gap-2">
            <ToggleSwitch
              :inputId="id(`link-${eintrag.id}`)"
              :modelValue="!!eintrag.link"
              @update:modelValue="(an) => (eintrag.link = an ? neuerLink({ label: 'Mehr erfahren' }) : null)"
            />
            <label :for="id(`link-${eintrag.id}`)" class="text-sm">Link anzeigen</label>
          </div>
          <AdminStartseiteLinkFeld v-if="eintrag.link" v-model="eintrag.link" :mitStil="false" />
        </template>
      </AdminStartseiteListe>
    </template>

    <!-- Kennzahlen -->
    <template v-else-if="block.typ === 'kennzahlen'">
      <AdminStartseiteFeld label="Überschrift" optional :feldId="id('titel')">
        <InputText :id="id('titel')" v-model="block.titel" />
      </AdminStartseiteFeld>
      <div class="flex items-center gap-2">
        <Checkbox v-model="block.nullwerteAusblenden" binary :inputId="id('null')" />
        <label :for="id('null')" class="text-sm">
          Kennzahlen mit dem Wert 0 ausblenden (z. B. solange noch nichts veröffentlicht wurde)
        </label>
      </div>
      <AdminStartseiteListe
        v-model="block.eintraege"
        :neu="neueKennzahl"
        elementName="Kennzahl"
        :titelVon="(k) => k.label"
        :max="6"
      >
        <template #default="{ eintrag }">
          <div class="grid gap-3 sm:grid-cols-2">
            <AdminStartseiteFeld
              label="Wert"
              :feldId="id(`quelle-${eintrag.id}`)"
              :hinweis="
                eintrag.quelle !== 'manuell' && aktuelleKennzahlen
                  ? `Aktuell: ${aktuelleKennzahlen[eintrag.quelle]}`
                  : ''
              "
            >
              <Select
                :inputId="id(`quelle-${eintrag.id}`)"
                v-model="eintrag.quelle"
                :options="KENNZAHL_QUELLEN"
                optionLabel="label"
                optionValue="value"
              />
            </AdminStartseiteFeld>
            <AdminStartseiteFeld
              v-if="eintrag.quelle === 'manuell'"
              label="Zahl"
              :feldId="id(`wert-${eintrag.id}`)"
            >
              <InputNumber :inputId="id(`wert-${eintrag.id}`)" v-model="eintrag.wert" locale="de-DE" />
            </AdminStartseiteFeld>
            <AdminStartseiteFeld label="Beschriftung" :feldId="id(`label-${eintrag.id}`)">
              <InputText :id="id(`label-${eintrag.id}`)" v-model="eintrag.label" />
            </AdminStartseiteFeld>
            <AdminStartseiteFeld
              label="Zusatz nach der Zahl"
              optional
              :feldId="id(`suffix-${eintrag.id}`)"
              hinweis="z. B. „+“ oder „ %“"
            >
              <InputText :id="id(`suffix-${eintrag.id}`)" v-model="eintrag.suffix" />
            </AdminStartseiteFeld>
            <AdminStartseiteFeld label="Icon" optional :feldId="id(`icon-${eintrag.id}`)">
              <AdminStartseiteIconAuswahl v-model="eintrag.icon" :inputId="id(`icon-${eintrag.id}`)" />
            </AdminStartseiteFeld>
          </div>
        </template>
      </AdminStartseiteListe>
    </template>

    <!-- Schritte -->
    <template v-else-if="block.typ === 'schritte'">
      <div class="grid gap-4 sm:grid-cols-2">
        <AdminStartseiteFeld label="Überschrift" optional :feldId="id('titel')">
          <InputText :id="id('titel')" v-model="block.titel" />
        </AdminStartseiteFeld>
        <AdminStartseiteFeld label="Untertitel" optional :feldId="id('untertitel')">
          <InputText :id="id('untertitel')" v-model="block.untertitel" />
        </AdminStartseiteFeld>
      </div>
      <AdminStartseiteListe
        v-model="block.schritte"
        :neu="neuerSchritt"
        elementName="Schritt"
        :titelVon="(s) => s.titel"
        :min="1"
        :max="4"
      >
        <template #default="{ eintrag }">
          <AdminStartseiteFeld label="Titel" :feldId="id(`titel-${eintrag.id}`)">
            <InputText :id="id(`titel-${eintrag.id}`)" v-model="eintrag.titel" />
          </AdminStartseiteFeld>
          <AdminStartseiteFeld label="Text" optional :feldId="id(`text-${eintrag.id}`)">
            <Textarea :id="id(`text-${eintrag.id}`)" v-model="eintrag.text" autoResize rows="2" />
          </AdminStartseiteFeld>
        </template>
      </AdminStartseiteListe>
    </template>

    <!-- FAQ -->
    <template v-else-if="block.typ === 'faq'">
      <AdminStartseiteFeld label="Überschrift" optional :feldId="id('titel')">
        <InputText :id="id('titel')" v-model="block.titel" />
      </AdminStartseiteFeld>
      <AdminStartseiteListe
        v-model="block.eintraege"
        :neu="neueFrage"
        elementName="Frage"
        :titelVon="(f) => f.frage"
        :max="30"
      >
        <template #default="{ eintrag }">
          <AdminStartseiteFeld label="Frage" :feldId="id(`frage-${eintrag.id}`)">
            <InputText :id="id(`frage-${eintrag.id}`)" v-model="eintrag.frage" />
          </AdminStartseiteFeld>
          <AdminStartseiteFeld label="Antwort">
            <RichContentEditor v-model="eintrag.antwort" />
          </AdminStartseiteFeld>
        </template>
      </AdminStartseiteListe>
    </template>

    <!-- Handlungsaufruf -->
    <template v-else-if="block.typ === 'aufruf'">
      <AdminStartseiteFeld label="Titel" :feldId="id('titel')">
        <InputText :id="id('titel')" v-model="block.titel" />
      </AdminStartseiteFeld>
      <AdminStartseiteFeld label="Text" optional :feldId="id('text')">
        <Textarea :id="id('text')" v-model="block.text" autoResize rows="2" />
      </AdminStartseiteFeld>
      <AdminStartseiteFeld label="Buttons" optional>
        <AdminStartseiteListe
          v-model="block.buttons"
          :neu="() => neuerLink({ stil: block.buttons.length ? 'sekundaer' : 'primaer' })"
          elementName="Button"
          :titelVon="(l) => l.label"
          :max="3"
        >
          <template #default="{ index }">
            <AdminStartseiteLinkFeld v-model="block.buttons[index]" />
          </template>
        </AdminStartseiteListe>
      </AdminStartseiteFeld>
    </template>

    <!-- Common: section background -->
    <AdminStartseiteFeld
      label="Hintergrund des Abschnitts"
      hinweis="„Akzent“ verwendet die Primärfarbe aus dem Branding."
    >
      <SelectButton
        v-model="block.hintergrund"
        :options="HINTERGRUENDE"
        optionLabel="label"
        optionValue="value"
        :allowEmpty="false"
      />
    </AdminStartseiteFeld>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import Button from 'openvue/button'
import Checkbox from 'openvue/checkbox'
import InputNumber from 'openvue/inputnumber'
import InputText from 'openvue/inputtext'
import Message from 'openvue/message'
import Select from 'openvue/select'
import SelectButton from 'openvue/selectbutton'
import Textarea from 'openvue/textarea'
import ToggleSwitch from 'openvue/toggleswitch'
import { useToast } from 'openvue/usetoast'
import {
  HINTERGRUENDE,
  KENNZAHL_QUELLEN,
  VIDEO_ANBIETER,
  VIDEO_DATENSCHUTZ_TEXTVORSCHLAG,
  neueFrage,
  neueKachel,
  neueKennzahl,
  neuerLink,
  neuerSchritt,
  parseVideoUrl
} from '@/utils/startseite'
import RichContentEditor from './RichContentEditor.vue'
import AdminStartseiteFeld from './AdminStartseiteFeld.vue'
import AdminStartseiteListe from './AdminStartseiteListe.vue'
import AdminStartseiteLinkFeld from './AdminStartseiteLinkFeld.vue'
import AdminStartseiteBildFeld from './AdminStartseiteBildFeld.vue'
import AdminStartseiteIconAuswahl from './AdminStartseiteIconAuswahl.vue'

const block = defineModel({ type: Object, required: true })
defineProps({
  // Current automatic figures, shown as a hint next to the source selection
  aktuelleKennzahlen: { type: Object, default: null }
})

const toast = useToast()

const id = (feld) => `abschnitt-${block.value.id}-${feld}`

const HERO_LAYOUTS = [
  { label: 'Zentriert', value: 'zentriert' },
  { label: 'Bild rechts', value: 'bild-rechts' },
  { label: 'Hintergrund', value: 'bild-hintergrund' }
]

const SEITENVERHAELTNISSE = [
  { label: 'Quer (16:9)', value: '16:9' },
  { label: 'Klassisch (4:3)', value: '4:3' },
  { label: 'Hochkant (9:16)', value: '9:16' }
]

const video = computed(() => (block.value.typ === 'video' ? parseVideoUrl(block.value.url) : null))

const kopiereDatenschutzText = async () => {
  try {
    await navigator.clipboard.write([
      new ClipboardItem({
        'text/html': new Blob([VIDEO_DATENSCHUTZ_TEXTVORSCHLAG], { type: 'text/html' }),
        'text/plain': new Blob(
          [VIDEO_DATENSCHUTZ_TEXTVORSCHLAG.replace(/<\/(h3|p)>/g, '\n\n').replace(/<[^>]+>/g, '')],
          { type: 'text/plain' }
        )
      })
    ])
    toast.add({
      severity: 'success',
      summary: 'Kopiert',
      detail: 'Textvorschlag in die Zwischenablage kopiert.',
      life: 3000
    })
  } catch {
    toast.add({
      severity: 'error',
      summary: 'Fehler',
      detail: 'Kopieren nicht möglich.',
      life: 3000
    })
  }
}
</script>
