<template>
  <div>
    <div class="grid grid-cols-8 gap-x-2 grid-flow-col">
      <div class="container col-span-2 w-fit mt-10">
        <Menu :model="items" class="w-fit">
          <template #item="{ item, props }">
            <router-link v-if="item.route" v-slot="{ href, navigate }" :to="item.route" custom>
              <a
                :href="href"
                v-bind="props.action"
                :class="{ 'bg-gray-200 font-semibold rounded-md': isActive(item) }"
                :aria-current="isActive(item) ? 'page' : undefined"
                @click="navigate"
              >
                <span :class="item.icon" />
                <span class="ml-2">{{ item.label }}</span>
              </a>
            </router-link>
          </template>
        </Menu>
      </div>
      <div class="container col-span-6">
        <BaseHeading> Einstellungen </BaseHeading>
        <Router-View />
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import Menu from 'openvue/menu'
import { useRoute } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const route = useRoute()

// Aktiv auch auf Unterseiten des Menüpunkts
const isActive = (item) => route.path === item.route || route.path.startsWith(`${item.route}/`)

const authStore = useAuthStore()

const allItems = [
  {
    label: 'Accounts',
    requiresRolleId: [1],
    items: [
      { label: 'Accountverwaltung', route: '/administration/accountverwaltung' },
      { label: 'Einladungen', route: '/administration/einladungen' },
      { label: 'Gruppen', route: '/administration/gruppen' }
    ]
  },
  {
    label: 'Kommune',
    requiresLocalSuperuser: true,
    items: [{ label: 'PDF-Logo', route: '/administration/pdf-logo' }]
  },
  {
    label: 'Einladungen',
    requiresRolleId: [2],
    items: [{ label: 'Einladungen', route: '/administration/einladungen' }]
  }
]

const items = computed(() =>
  allItems.filter((group) =>
    group.requiresLocalSuperuser
      ? authStore.istKommunaleAdmin
      : group.requiresRolleId.includes(authStore.effectiveRolleId) ||
      (authStore.effectiveIsLocalSuperuser && group.requiresRolleId.includes(1))
  )
)
</script>
