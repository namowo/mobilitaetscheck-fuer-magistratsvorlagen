<template>
  <div>
    <div class="grid grid-cols-8 gap-x-2 grid-flow-col">
      <div class="container col-span-2 w-fit mt-10">
        <Menu :model="items" class="w-fit">
          <template #item="{ item, props }">
            <router-link v-if="item.route" v-slot="{ href, navigate }" :to="item.route" custom>
              <a :href="href" v-bind="props.action" @click="navigate">
                <span :class="item.icon" />
                <span class="ml-2">{{ item.label }}</span>
              </a>
            </router-link>
            <a v-else :href="item.url" :target="item.target" v-bind="props.action">
              <span :class="item.icon" />
              <span class="ml-2">{{ item.label }}</span>
            </a>
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
import { useAuthStore } from '@/stores/auth'

const authStore = useAuthStore()

const allItems = [
  {
    label: 'Kommune',
    requiresRolleId: [1],
    items: [
      {
        label: 'Gebiete',
        route: '/einstellungen/gemeinde-gebiet'
      }
    ]
  },
  {
    label: 'Mobilitätscheck',
    requiresRolleId: [1],
    items: [
      {
        label: 'Leitziele',
        route: '/einstellungen/leitziel-sets'
      },
      {
        label: 'Textblöcke',
        route: '/einstellungen/textblock'
      },
      {
        label: 'Indikatoren',
        route: '/einstellungen/indikator'
      },
      {
        label: 'Tags',
        route: '/einstellungen/tag'
      }
    ]
  },
  {
    label: 'Administration',
    requiresRolleId: [1],
    items: [
      {
        label: 'Accountverwaltung',
        route: '/einstellungen/accountverwaltung'
      },
      {
        label: 'Einladungen',
        route: '/einstellungen/einladungen'
      },
      {
        label: 'Gruppen',
        route: '/einstellungen/gruppen'
      }
    ]
  },
  {
    label: 'Einladungen',
    requiresRolleId: [2],
    items: [
      {
        label: 'Einladungen',
        route: '/einstellungen/einladungen'
      }
    ]
  }
]

const items = computed(() =>
  allItems.filter(
    (group) =>
      group.requiresRolleId.includes(authStore.effectiveRolleId) ||
      (authStore.isLocalSuperuser && group.requiresRolleId.includes(1))
  )
)
</script>

<style></style>
