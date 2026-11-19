<template>
  <Toolbar
    style="border-radius: 0.5rem; background-color: rgb(var(--primary-base))"
    class="w-full relative-toolbar"
  >
    <template #start>
      <div class="flex items-center gap-3 text-white">
        <template v-if="brandingStore.menueleisteLogos.length > 0">
          <template v-for="logo in brandingStore.menueleisteLogos" :key="logo.id">
            <BrandingLogoLink v-if="logo.link" :href="logo.link">
              <img :src="logo.asset.url" alt="Logo" class="h-10 max-w-32 object-contain" />
            </BrandingLogoLink>
            <router-link v-else :to="{ name: 'startseite' }">
              <img :src="logo.asset.url" alt="Logo" class="h-10 max-w-32 object-contain" />
            </router-link>
          </template>
        </template>
        <router-link v-else :to="{ name: 'startseite' }" class="menuItem-active-link">
          <img width="120px" :src="defaultLogo" alt="Logo" />
        </router-link>
      </div>
    </template>
    <template #center>
      <div class="flex items-center gap-2">
        <template v-if="authStore.isLoggedIn">
          <router-link
            v-if="![3].includes(authStore.effectiveRolleId) || authStore.effectiveIsLocalSuperuser"
            :to="{ name: 'magistratsvorlage-liste' }"
          >
            <Button label="Magistratsvorlagen" data-tour="nav-magistratsvorlagen" />
          </router-link>
          <router-link v-if="authStore.effectiveRolleId === 3" :to="{ name: 'admin-dashboard' }">
            <Button label="Systemadministration" />
          </router-link>
        </template>
      </div>
    </template>

    <template #end>
      <div v-if="authStore.isLoggedIn" class="flex items-center gap-2">
        <router-link
          v-if="[1].includes(authStore.effectiveRolleId) || authStore.effectiveIsLocalSuperuser"
          :to="{ name: 'leitziel-sets' }"
        >
          <Button
            v-tooltip.left="'Gebiete, Leitziele, Textbausteine, Indikatoren und Tags Ihrer Kommune verwalten'"
            label="Verwaltung"
            icon="pi pi-sliders-h"
            data-tour="nav-verwaltung"
          />
        </router-link>
        <router-link
          v-if="[1].includes(authStore.effectiveRolleId) || authStore.effectiveIsLocalSuperuser"
          :to="{ name: 'accountverwaltung' }"
        >
          <Button
            v-tooltip.left="'Accounts, Einladungen und Gruppen Ihrer Kommune verwalten'"
            label="Einstellungen"
            icon="pi pi-users"
            data-tour="nav-einstellungen"
          />
        </router-link>

        <Avatar
          v-tooltip.right="'Profil und Abmelden'"
          :label="authStore.userInitialien"
          shape="circle"
          class="cursor-pointer"
          data-tour="profil-menue"
          @click="toggle"
        />

        <Popover ref="op">
          <div class="w-60 flex flex-col">
            <!-- Who is logged in -->
            <div class="flex items-center gap-3 px-2 pb-3">
              <Avatar :label="authStore.userInitialien" shape="circle" class="shrink-0" />
              <div class="min-w-0">
                <div class="text-xs text-gray-500">Angemeldet als</div>
                <div class="truncate text-sm font-medium text-gray-800" :title="authStore.userEmail">
                  {{ authStore.userEmail }}
                </div>
              </div>
            </div>

            <div class="border-t border-gray-200 py-1">
              <!-- custom: avoid the router-link-active styling of the menu bar links -->
              <router-link v-slot="{ navigate }" :to="{ name: 'profil' }" custom>
                <button type="button" class="menu-eintrag" @click="schliessenUnd(navigate)">
                  <i class="pi pi-user" />
                  <span>Profil</span>
                </button>
              </router-link>
              <button
                v-if="wizardManuellStartbar"
                type="button"
                class="menu-eintrag"
                @click="startEinfuehrung"
              >
                <i class="pi pi-compass" />
                <span>Einführung starten</span>
              </button>
            </div>

            <div class="border-t border-gray-200 pt-1">
              <button type="button" class="menu-eintrag menu-eintrag--abmelden" @click="abmelden">
                <i class="pi pi-sign-out" />
                <span>Abmelden</span>
              </button>
            </div>
          </div>
        </Popover>
      </div>
      <div v-else class="flex items-center gap-2">
        <router-link :to="{ name: 'anmelden' }">
          <Button label="Anmelden" icon="pi pi-sign-in" />
        </router-link>
      </div>
    </template>
  </Toolbar>
</template>

<script setup>
import { ref } from 'vue'
import { useAuthStore } from '@/stores/auth'
import { useBrandingStore } from '@/stores/branding'
import { useStartWizard } from '@/composables/startWizard'
import Avatar from 'openvue/avatar'
import Button from 'openvue/button'
import Toolbar from 'openvue/toolbar'
import Popover from 'openvue/popover'
import BrandingLogoLink from './BrandingLogoLink.vue'
import defaultLogo from '../assets/logos/pimoo-logo-invertiert.png'

const authStore = useAuthStore()
const brandingStore = useBrandingStore()

const op = ref()

const {
  open: openWizard,
  available: wizardAvailable,
  manuellStartbar: wizardManuellStartbar,
  refreshStatus
} = useStartWizard()
const startEinfuehrung = () => {
  op.value.hide()
  openWizard(0)
}

const schliessenUnd = (navigate) => {
  op.value.hide()
  navigate()
}

const abmelden = () => {
  op.value.hide()
  authStore.logout()
}

const toggle = (event) => {
  if (wizardAvailable.value) refreshStatus() // keeps the "Einführung starten" entry current
  op.value.toggle(event)
}
</script>

<style scoped>
.router-link-exact-active.menuItem-active-link {
  @apply text-white;
}
.router-link-active,
.router-link-exact-active {
  @apply block py-2 px-3 text-white bg-blue-700 rounded md:bg-transparent md:text-blue-700 md:p-0 dark:text-white md:dark:text-blue-500;
}

.menu-eintrag {
  @apply flex w-full items-center gap-3 rounded-md px-2 py-2 text-left text-sm text-gray-700 transition-colors;
}
.menu-eintrag:hover,
.menu-eintrag:focus-visible {
  @apply bg-gray-100 text-gray-900 outline-none;
}
.menu-eintrag i {
  @apply w-4 text-center text-gray-500;
}
.menu-eintrag--abmelden,
.menu-eintrag--abmelden i {
  @apply text-red-700;
}
.menu-eintrag--abmelden:hover,
.menu-eintrag--abmelden:focus-visible {
  @apply bg-red-50 text-red-800;
}

.relative-toolbar {
  position: relative;
  flex-wrap: wrap;
  row-gap: 0.5rem;
}

.relative-toolbar :deep(.p-toolbar-center) {
  flex-wrap: wrap;
}

/* Only center absolutely when there is enough room for all three areas */
@media (min-width: 1280px) {
  .relative-toolbar :deep(.p-toolbar-center) {
    position: absolute;
    left: 50%;
    transform: translateX(-50%);
    max-width: calc(100% - 2rem);
  }
}
</style>
