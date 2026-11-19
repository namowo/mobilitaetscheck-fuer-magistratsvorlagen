<template>
  <div>
    <div class="flex gap-4 items-center mb-2">
      <BaseSubheading>Accountverwaltung</BaseSubheading>
    </div>
    <p class="mb-5 text-sm text-gray-600">
      Hier sehen Sie alle Benutzerkonten Ihrer Kommune. Sie können die Rolle und Gruppe eines Kontos
      ändern und festlegen, ob es Rechte als kommunaler Administrator erhält.
    </p>
    <AccountListe />
  </div>
</template>

<script setup>
import AccountListe from '@/components/AccountListe.vue'
</script>

<style></style>
