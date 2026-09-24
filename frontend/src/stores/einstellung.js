import { ref } from 'vue'
import { defineStore } from 'pinia'
import { useTitle } from '@vueuse/core'
import { apiClient } from '@/services/axios'
import { applyThemeColor } from '@/utils/theme'

export const useEinstellungStore = defineStore('einstellung', () => {
  const einstellung = ref({})
  const isLoaded = ref(false)
  const title = useTitle()

  async function fetchEinstellung() {
    try {
      const res = await apiClient.get('/public/plattform-einstellung')
      einstellung.value = res.data
      if (einstellung.value.themeColor) {
        applyThemeColor(einstellung.value.themeColor)
      }
      if (einstellung.value.webAppTitle) {
        title.value = einstellung.value.webAppTitle
        try {
          localStorage.setItem('brandingWebAppTitle', einstellung.value.webAppTitle)
        } catch {
          // localStorage unavailable, ignore
        }
      } else {
        try {
          localStorage.removeItem('brandingWebAppTitle')
        } catch {
          // localStorage unavailable, ignore
        }
      }
    } catch {
      einstellung.value = {}
    } finally {
      isLoaded.value = true
    }
  }

  return { einstellung, isLoaded, fetchEinstellung }
})
