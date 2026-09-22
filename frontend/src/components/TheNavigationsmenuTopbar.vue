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
        <router-link :to="{ name: 'startseite' }">
          <Button label="Startseite" severity="primary" />
        </router-link>
        <template v-if="authStore.isLoggedIn">
          <router-link
            v-if="![3].includes(authStore.userRolleId)"
            :to="{ name: 'magistratsvorlage-liste' }"
          >
            <Button label="Magistratsvorlagen" />
          </router-link>
          <router-link v-if="[3].includes(authStore.userRolleId)" :to="{ name: 'admin-kommunen' }">
            <Button label="Administration" />
          </router-link>
        </template>
      </div>
    </template>

    <template #end>
      <div v-if="authStore.isLoggedIn" class="flex items-center gap-2">
        <router-link v-if="[1].includes(authStore.userRolleId)" :to="{ name: 'leitziel-sets' }">
          <Button v-tooltip.left="'Einstellungen'" icon="pi pi-cog" />
        </router-link>
        <router-link v-if="[2].includes(authStore.userRolleId)" :to="{ name: 'einladungen' }">
          <Button v-tooltip.left="'Einladungen'" icon="pi pi-user-plus" />
        </router-link>

        <Avatar
          v-tooltip.right="'Profil und Abmelden'"
          :label="authStore.userInitialien"
          shape="circle"
          @click="toggle"
        />

        <Popover ref="op">
          <div class="flex flex-col gap-4 w-[8rem]">
            <router-link :to="{ name: 'profil' }">
              <Button icon="pi pi-user" label="Profil" class="w-full" text plain />
            </router-link>
            <Button
              icon="pi pi-sign-out"
              label="Abmelden"
              class="w-full"
              @click="authStore.logout"
            />
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
import Avatar from 'openvue/avatar'
import Button from 'openvue/button'
import Toolbar from 'openvue/toolbar'
import Popover from 'openvue/popover'
import BrandingLogoLink from './BrandingLogoLink.vue'
import defaultLogo from '../assets/logos/pimoo-logo-invertiert.png'

const authStore = useAuthStore()
const brandingStore = useBrandingStore()

const op = ref()

const toggle = (event) => {
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

.relative-toolbar {
  position: relative;
}

.relative-toolbar :deep(.p-toolbar-center) {
  position: absolute;
  left: 50%;
  transform: translateX(-50%);
  max-width: calc(100% - 2rem);
}

@media (max-width: 767px) {
  .relative-toolbar :deep(.p-toolbar-center) {
    position: static;
    transform: none;
    max-width: none;
  }
}
</style>
