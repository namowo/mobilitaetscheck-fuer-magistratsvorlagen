<template>
  <Dialog
    v-model:visible="visible"
    modal
    :closable="false"
    :draggable="false"
    :style="{ width: '40rem', maxWidth: '95vw' }"
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
            </template>
            <template v-else>Sehr gut – Ihre Kommune ist vollständig eingerichtet.</template>
          </p>
          <ul class="flex flex-col gap-2">
            <li
              v-for="s in checklistSchritte"
              :key="s.key"
              class="flex items-center gap-3 rounded border border-gray-200 p-2"
            >
              <i
                v-if="status[s.statusKey]"
                class="pi pi-check-circle text-green-600"
                aria-label="erledigt"
              />
              <i
                v-else
                :class="[
                  s.optional ? 'pi pi-circle text-gray-400' : 'pi pi-exclamation-triangle text-amber-600'
                ]"
                aria-label="offen"
              />
              <span class="flex-1" :class="status[s.statusKey] ? 'text-gray-500 line-through' : ''">
                {{ s.title }}
                <span v-if="!status[s.statusKey] && s.optional" class="text-xs text-gray-500">
                  (optional)
                </span>
              </span>
              <Button
                v-if="!status[s.statusKey] && s.action"
                :label="s.action.label"
                size="small"
                outlined
                @click="goTo(s.action.to)"
              />
            </li>
          </ul>
        </template>
      </template>

      <p v-for="(p, i) in currentStep.paragraphs" :key="i" class="text-gray-800 leading-relaxed">
        {{ p }}
      </p>

      <div v-if="currentStep.action || currentStep.actions" class="flex flex-wrap gap-2">
        <Button
          v-for="a in currentStep.actions || [currentStep.action]"
          :key="a.label"
          :label="a.label"
          icon="pi pi-arrow-right"
          iconPos="right"
          outlined
          @click="goTo(a.to)"
        />
      </div>
    </div>

    <template #footer>
      <div class="flex w-full items-center justify-between gap-2">
        <Button label="Nicht mehr anzeigen" text severity="secondary" size="small" @click="skip" />
        <div class="flex gap-2">
          <Button v-if="!isFirst" label="Zurück" severity="secondary" outlined @click="prev" />
          <Button v-if="!isLast" label="Weiter" icon="pi pi-arrow-right" iconPos="right" @click="next" />
          <Button v-else label="Fertig" icon="pi pi-check" @click="finish" />
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
</template>

<script setup>
import { computed, watch } from 'vue'
import { useRouter } from 'vue-router'
import Dialog from 'openvue/dialog'
import Button from 'openvue/button'
import { useAuthStore } from '@/stores/auth'
import { useStartWizard } from '@/composables/startWizard'

const router = useRouter()
const authStore = useAuthStore()

const {
  available,
  visible,
  stepIndex,
  status,
  statusLoaded,
  resumable,
  steps,
  currentStep,
  isFirst,
  isLast,
  close,
  resume,
  finish,
  skip,
  next,
  prev,
  autoOpenIfNeeded
} = useStartWizard()

// Steps with a status (done/open) feed the final overview
const checklistSchritte = computed(() =>
  steps.value.flatMap((s) => s.checklistItems || (s.statusKey ? [s] : []))
)
const offeneSchritte = computed(() => checklistSchritte.value.filter((s) => !status.value[s.statusKey]))

// Leave the wizard to do the task; reopening resumes at the same step.
const goTo = (to) => {
  close()
  router.push(to)
}

// Open automatically once the user is logged in and verified (also on page reload)
watch(
  () => [authStore.isLoggedIn, authStore.isVerified, authStore.userId, authStore.effectiveRolleId],
  autoOpenIfNeeded,
  { immediate: true }
)
</script>
