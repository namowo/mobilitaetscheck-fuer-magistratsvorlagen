<template>
  <Dialog
    v-model:visible="visible"
    modal
    :closable="false"
    :draggable="false"
    :style="{ width: '40rem', maxWidth: '95vw' }"
    :pt="{ footer: { class: 'border-t border-gray-200 pt-4' } }"
    @hide="close"
  >
    <template #header>
      <div class="flex items-center gap-3">
        <i :class="[currentStep?.icon, 'text-2xl']" style="color: rgb(var(--primary-base))" />
        <span class="text-xl font-semibold">{{ currentStep?.title }}</span>
      </div>
    </template>

    <div v-if="currentStep" class="flex flex-col gap-4">
      <!-- Progress -->
      <div class="flex items-center gap-1" role="progressbar" :aria-valuenow="stepIndex + 1" :aria-valuemax="steps.length">
        <button
          v-for="(s, i) in steps"
          :key="s.key"
          type="button"
          class="h-2 flex-1 rounded-full transition-colors"
          :class="i <= stepIndex ? 'bg-blue-700' : 'bg-gray-200'"
          :aria-label="`Schritt ${i + 1}: ${s.title}`"
          @click="stepIndex = i"
        />
      </div>
      <div class="text-xs text-gray-500">Schritt {{ stepIndex + 1 }} von {{ steps.length }}</div>

      <!-- Status badge -->
      <div v-if="currentStep.statusKey && statusLoaded" class="flex items-center gap-2 text-sm">
        <template v-if="status[currentStep.statusKey]">
          <i class="pi pi-check-circle text-green-600" />
          <span class="text-green-700">Bereits erledigt</span>
        </template>
        <template v-else>
          <i
            :class="[
              currentStep.optional ? 'pi pi-info-circle text-gray-500' : 'pi pi-exclamation-triangle text-amber-600'
            ]"
          />
          <span :class="currentStep.optional ? 'text-gray-600' : 'text-amber-700'">
            {{ currentStep.optional ? 'Noch nicht erledigt (optional)' : 'Noch offen' }}
          </span>
        </template>
      </div>
      <span v-else-if="currentStep.optional" class="text-sm text-gray-500">Optional</span>

      <!-- Final overview: everything that is still to do -->
      <template v-if="currentStep.checklist">
        <p v-if="!statusLoaded" class="text-gray-600">Status wird geladen …</p>
        <template v-else>
          <p class="text-gray-800 leading-relaxed">
            <template v-if="offeneSchritte.length">
              Folgendes ist noch offen. Pflichtschritte sind markiert, optionale können Sie auch später erledigen.
              Klicken Sie auf einen offenen Punkt, um direkt dorthin zu gelangen.
            </template>
            <template v-else>Sehr gut – Ihre Kommune ist vollständig eingerichtet.</template>
          </p>
          <ul class="m-0 flex list-none flex-col p-0">
            <li v-for="s in checklistSchritte" :key="s.key">
              <!-- Open task: the whole row (incl. its status icon) leads to the task -->
              <button
                v-if="!status[s.statusKey] && s.action"
                type="button"
                class="aufgabe aufgabe--offen group"
                :title="s.action.label"
                :aria-label="`${s.title}${s.optional ? ' (optional)' : ''} – ${s.action.label}`"
                @click="goTo(s.action)"
              >
                <!-- Show/hide on wrapper spans: PrimeIcons' .pi display rule would override `hidden` -->
                <span class="aufgabe__icon">
                  <span class="group-hover:hidden group-focus-visible:hidden">
                    <i
                      :class="
                        s.optional ? 'pi pi-circle text-gray-400' : 'pi pi-exclamation-triangle text-amber-600'
                      "
                    />
                  </span>
                  <span class="hidden group-hover:inline group-focus-visible:inline">
                    <i class="pi pi-arrow-circle-right" style="color: rgb(var(--primary-base))" />
                  </span>
                </span>
                <span class="flex-1">
                  {{ s.title }}
                  <span v-if="s.optional" class="text-xs text-gray-500">(optional)</span>
                </span>
                <i class="pi pi-chevron-right text-xs text-gray-400 group-hover:text-gray-700" />
              </button>

              <div v-else class="aufgabe">
                <span class="aufgabe__icon">
                  <i
                    v-if="status[s.statusKey]"
                    class="pi pi-check-circle text-green-600"
                    aria-label="erledigt"
                  />
                  <i v-else class="pi pi-circle text-gray-400" aria-label="offen" />
                </span>
                <span class="flex-1" :class="status[s.statusKey] ? 'text-gray-500 line-through' : ''">
                  {{ s.title }}
                </span>
              </div>
            </li>
          </ul>
        </template>
      </template>

      <p v-for="(p, i) in currentStep.paragraphs" :key="i" class="text-gray-800 leading-relaxed">
        {{ p }}
      </p>

      <!-- Einstellungen direkt im Schritt ändern -->
      <EinstellungenFremdeEintraege v-if="currentStep.einstellungen === 'inhalteTeilen'" kompakt />

      <div v-if="currentStep.action || currentStep.actions" class="flex flex-col gap-2">
        <div class="flex flex-wrap gap-2">
          <Button
            v-for="a in currentStep.actions || [currentStep.action]"
            :key="a.label"
            :label="a.label"
            icon="pi pi-arrow-right"
            iconPos="right"
            outlined
            @click="goTo(a)"
          />
        </div>
        <p
          v-if="(currentStep.actions || [currentStep.action]).some((a) => a.spotlight)"
          class="m-0 flex items-center gap-2 text-sm text-gray-500"
        >
          <i class="pi pi-lightbulb" />
          Auf der Seite zeigen wir Ihnen, wo es weitergeht. Danach können Sie die Einführung fortsetzen.
        </p>
      </div>
    </div>

    <template #footer>
      <!-- Small screens: navigation on top (full width), dismiss link below -->
      <div class="flex w-full flex-col-reverse gap-2 sm:flex-row sm:items-center sm:justify-between">
        <Button label="Nicht mehr anzeigen" text severity="secondary" size="small" @click="beenden" />
        <div class="flex gap-2">
          <Button
            v-if="!isFirst"
            label="Zurück"
            severity="secondary"
            outlined
            class="flex-1 sm:flex-none"
            @click="prev"
          />
          <Button
            v-if="!isLast"
            label="Weiter"
            icon="pi pi-arrow-right"
            iconPos="right"
            class="flex-1 sm:flex-none"
            @click="next"
          />
          <Button v-else label="Fertig" icon="pi pi-check" class="flex-1 sm:flex-none" @click="beenden" />
        </div>
      </div>
    </template>
  </Dialog>

  <div
    v-if="available && resumable && !visible && authStore.isLoggedIn"
    class="mb-2 flex flex-wrap items-center gap-2 rounded border border-blue-200 bg-blue-50 p-3 text-sm text-blue-900"
    role="status"
  >
    <i class="pi pi-compass shrink-0" />
    <span class="flex-1">
      <strong>Einrichtungsassistent:</strong>
      Sie sind bei Schritt {{ stepIndex + 1 }} von {{ steps.length }} – „{{ currentStep?.title }}“.
    </span>
    <Button
      label="Fortsetzen"
      icon="pi pi-arrow-right"
      iconPos="right"
      size="small"
      severity="secondary"
      @click="resume"
    />
  </div>

  <!-- Docked panel while the user works on a step's task -->
  <Teleport to="body">
    <Transition name="wizard-dock">
      <aside
        v-if="available && angedockt && !visible && authStore.isLoggedIn && currentStep"
        class="wizard-dock"
        aria-label="Einführung"
      >
        <div class="flex items-center gap-2 border-b border-gray-200 px-4 py-2">
          <i class="pi pi-compass" style="color: rgb(var(--primary-base))" />
          <span class="flex-1 text-xs font-medium text-gray-500">
            Einführung · Schritt {{ stepIndex + 1 }} von {{ steps.length }}
          </span>
          <Button
            v-tooltip.top="'Einführung groß anzeigen'"
            icon="pi pi-window-maximize"
            text
            rounded
            size="small"
            severity="secondary"
            aria-label="Einführung groß anzeigen"
            @click="aufklappen"
          />
          <Button
            v-tooltip.top="'Ausblenden'"
            icon="pi pi-minus"
            text
            rounded
            size="small"
            severity="secondary"
            aria-label="Einführung ausblenden"
            @click="minimieren"
          />
        </div>

        <div class="flex flex-col gap-3 px-4 py-3">
          <div class="flex items-center gap-2 font-semibold text-gray-800">
            <i :class="currentStep.icon" />
            <span>{{ currentStep.title }}</span>
          </div>

          <!-- Live status of the task(s) of this step -->
          <ul v-if="dockAufgaben.length && statusLoaded" class="m-0 flex list-none flex-col gap-1 p-0 text-sm">
            <li v-for="a in dockAufgaben" :key="a.key" class="flex items-center gap-2">
              <i v-if="status[a.statusKey]" class="pi pi-check-circle text-green-600" />
              <i v-else class="pi pi-circle text-gray-400" />
              <span :class="status[a.statusKey] ? 'text-green-700' : 'text-gray-700'">
                {{ dockAufgaben.length > 1 ? a.title : status[a.statusKey] ? 'Erledigt' : 'Noch offen' }}
              </span>
            </li>
          </ul>

          <p class="m-0 text-sm text-gray-600" role="status" aria-live="polite">
            <template v-if="dockErledigt">Sehr gut! Weiter geht's mit dem nächsten Schritt.</template>
            <template v-else>Erledigen Sie diesen Schritt auf der Seite und klicken Sie dann auf „Weiter“.</template>
          </p>

          <div v-if="dockAktionen.length" class="flex flex-wrap gap-1">
            <Button
              v-for="a in dockAktionen"
              :key="a.label"
              :label="a.label"
              icon="pi pi-map-marker"
              size="small"
              text
              @click="goTo(a)"
            />
          </div>
        </div>

        <div class="flex items-center justify-between gap-2 border-t border-gray-200 px-4 py-2">
          <Button v-if="!isFirst" label="Zurück" size="small" text severity="secondary" @click="dockZurueck" />
          <span v-else />
          <Button
            :label="isLast ? 'Zur Übersicht' : 'Weiter'"
            icon="pi pi-arrow-right"
            iconPos="right"
            size="small"
            :class="{ 'wizard-dock__weiter--bereit': dockErledigt }"
            @click="dockWeiter"
          />
        </div>
      </aside>
    </Transition>
  </Teleport>
</template>

<script setup>
import { computed, watch, onBeforeUnmount } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import Dialog from 'openvue/dialog'
import Button from 'openvue/button'
import { useAuthStore } from '@/stores/auth'
import { useStartWizard } from '@/composables/startWizard'
import { useWizardSpotlight } from '@/composables/wizardSpotlight'
import EinstellungenFremdeEintraege from '@/components/EinstellungenFremdeEintraege.vue'

const router = useRouter()
const route = useRoute()
const authStore = useAuthStore()

const {
  available,
  visible,
  stepIndex,
  manuellStartbar,
  status,
  statusLoaded,
  resumable,
  angedockt,
  steps,
  currentStep,
  isFirst,
  isLast,
  close,
  andocken,
  aufklappen,
  minimieren,
  refreshStatus,
  resume,
  finish,
  next,
  prev,
  autoOpenIfNeeded
} = useStartWizard()

// Steps with a status (done/open) feed the final overview
const checklistSchritte = computed(() =>
  steps.value.flatMap((s) => s.checklistItems || (s.statusKey ? [s] : []))
)
const offeneSchritte = computed(() => checklistSchritte.value.filter((s) => !status.value[s.statusKey]))

const { markieren, zeigen } = useWizardSpotlight()

// While a step is shown, ring the menu entry where its task can be found
watch(
  () => (visible.value ? currentStep.value?.zeigt : null),
  (zeigt) => markieren(zeigt || null),
  { immediate: true }
)

// Leave the dialog to do the task and point at the element to use there; the wizard
// stays available as a docked panel, so the user can go on without the banner.
const goTo = (action) => {
  andocken()
  zeigen(action.spotlight || null)
  router.push(action.to)
}

// ---- Docked panel ----
const dockAufgaben = computed(() => {
  const s = currentStep.value
  if (!s) return []
  return s.checklistItems || (s.statusKey ? [s] : [])
})
const dockAktionen = computed(() => {
  const s = currentStep.value
  return (s?.actions || (s?.action ? [s.action] : [])).filter(Boolean)
})
// Required tasks done (or, for steps with only optional tasks, at least one of them)
const dockErledigt = computed(() => {
  const a = dockAufgaben.value
  if (!a.length || !statusLoaded.value) return false
  const pflicht = a.filter((x) => !x.optional)
  return pflicht.length
    ? pflicht.every((x) => status.value[x.statusKey])
    : a.some((x) => status.value[x.statusKey])
})

const dockWeiter = () => {
  next()
  aufklappen() // show the next step's explanation
}
const dockZurueck = () => {
  prev()
  aufklappen()
}

// Keep the panel's status current while the user works: after saves and page changes
let statusTimer = null
const statusAktualisieren = () => {
  if (!angedockt.value) return
  clearTimeout(statusTimer)
  statusTimer = setTimeout(refreshStatus, 400)
}
window.addEventListener('api-daten-geaendert', statusAktualisieren)
watch(() => route.fullPath, statusAktualisieren)
watch(angedockt, statusAktualisieren)
onBeforeUnmount(() => {
  window.removeEventListener('api-daten-geaendert', statusAktualisieren)
  clearTimeout(statusTimer)
})

// Finishing or dismissing: show where the wizard can be reopened, if the profile menu
// offers it.
const beenden = () => {
  finish()
  if (manuellStartbar.value) {
    zeigen({
      ziel: 'profil-menue',
      title: 'Einführung wieder öffnen',
      text: 'Über Ihr Profil-Menü können Sie die Einführung jederzeit erneut starten.'
    })
  }
}

// Open automatically once the user is logged in and verified (also on page reload)
watch(
  () => [authStore.isLoggedIn, authStore.isVerified, authStore.userId, authStore.effectiveRolleId],
  autoOpenIfNeeded,
  { immediate: true }
)
</script>

<style scoped>
.aufgabe {
  @apply flex w-full items-center gap-3 rounded-md px-2 py-2 text-left text-gray-800;
}
.aufgabe--offen {
  @apply transition-colors hover:bg-gray-100 focus-visible:bg-gray-100 focus-visible:outline-none;
}
.aufgabe__icon {
  @apply flex w-5 shrink-0 justify-center text-lg;
}

.wizard-dock {
  position: fixed;
  right: 1rem;
  bottom: calc(1rem + env(safe-area-inset-bottom, 0px));
  z-index: 1000;
  width: min(22rem, calc(100vw - 2rem));
  border-radius: 0.75rem;
  border: 1px solid rgb(229 231 235);
  background: #fff;
  box-shadow: 0 12px 32px rgba(0, 0, 0, 0.18);
}
.wizard-dock-enter-active,
.wizard-dock-leave-active {
  transition:
    opacity 0.2s ease,
    transform 0.2s ease;
}
.wizard-dock-enter-from,
.wizard-dock-leave-to {
  opacity: 0;
  transform: translateY(0.75rem);
}
.wizard-dock__weiter--bereit {
  animation: wizard-dock-bereit 1.6s ease-out infinite;
}
@keyframes wizard-dock-bereit {
  from {
    box-shadow: 0 0 0 0 rgb(var(--primary-base) / 0.5);
  }
  to {
    box-shadow: 0 0 0 10px rgb(var(--primary-base) / 0);
  }
}
@media (prefers-reduced-motion: reduce) {
  .wizard-dock-enter-active,
  .wizard-dock-leave-active {
    transition: none;
  }
  .wizard-dock__weiter--bereit {
    animation: none;
  }
}
</style>
