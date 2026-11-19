<template>
  <div class="max-w-3xl mx-auto">
    <BaseSubheading>Profil</BaseSubheading>
    <p class="text-sm text-gray-600 mb-5">
      Verwalten Sie hier Ihre persönlichen Angaben und Ihr Passwort.
    </p>

    <div class="flex flex-col gap-6">
      <AuthAccountDaten />
      <AuthPasswortZuruecksetzen :changePassword="true" />
    </div>
  </div>
</template>

<script setup>
import AuthAccountDaten from '@/components/AuthAccountDaten.vue'
import AuthPasswortZuruecksetzen from '@/components/AuthPasswortZuruecksetzen.vue'
</script>
