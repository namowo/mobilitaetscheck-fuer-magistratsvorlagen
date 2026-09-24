<template>
  <div class="min-h-screen flex flex-col">
    <div class="max-w-6xl mx-auto p-1 w-full flex-1">
      <TheNavigationsmenuTopbar class="w-full mb-2" />
      <TheLeitzieleFehlenBanner class="mb-2" />
      <TheDokumentationHinweisBanner class="mb-2" />
      <Toast position="bottom-right" />
      <ConfirmDialog />
      <RouterView />
    </div>
    <TheFooter />
  </div>
</template>

<script setup>
import { RouterView } from 'vue-router'
import ConfirmDialog from 'openvue/confirmdialog'
import Toast from 'openvue/toast'
import TheNavigationsmenuTopbar from './components/TheNavigationsmenuTopbar.vue'
import TheLeitzieleFehlenBanner from './components/TheLeitzieleFehlenBanner.vue'
import TheDokumentationHinweisBanner from './components/TheDokumentationHinweisBanner.vue'
import TheFooter from './components/TheFooter.vue'
</script>

<style>
.route-enter-from {
  opacity: 0;
  transform: translateY(-30px);
}
.route-leave-to {
  opacity: 0;
  transform: translateY(30px);
}

.route-enter-active {
  transition: all 0.3s ease-out;
}

.route-leave-active {
  transition: all 0.3s ease-in;
}

.route-enter-to,
.route-leave-from {
  opacity: 1;
  transform: translateY(0);
}
</style>
