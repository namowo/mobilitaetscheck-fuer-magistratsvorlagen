<template>
  <div class="mx-auto p-6">
    <div class="flex items-center gap-5 mb-4">
      <BaseHeading class="mb-0">Magistratsvorlagen</BaseHeading>
      <RouterLink
        v-if="authStore.effectiveRolleId === 1 || authStore.effectiveIsLocalSuperuser"
        :to="{ name: 'magistratsvorlage-neu' }"
        class="flex"
      >
        <Button
          v-tooltip="'Neue Magistratsvorlage anlegen'"
          icon="pi pi-plus"
          rounded
          aria-label="Neue Magistratsvorlage anlegen"
        />
      </RouterLink>
    </div>
    <MagistrasvorlageListe />
  </div>
</template>

<script setup>
import MagistrasvorlageListe from '@/components/MagistrasvorlageListe.vue'
import Button from 'openvue/button'
import { useAuthStore } from '@/stores/auth'

const authStore = useAuthStore()
</script>

<style></style>
