import { ref, computed } from 'vue'
import { defineStore } from 'pinia'
import { useTitle } from '@vueuse/core'
import { apiClient } from '@/services/axios'
import { applyThemeColor } from '@/utils/theme'

export const STANDARD_APP_NAME = 'MobiChecks-Hessen'

export const useEinstellungStore = defineStore('einstellung', () => {
  const einstellung = ref({})
  const isLoaded = ref(false)
  const title = useTitle()

  // Name of the tool as shown in the UI (Branding → Anwendungstitel). "Mobilitätscheck"
  // refers to the PDF output only, so the fallback is the tool's name.
  const appName = computed(() => einstellung.value.webAppTitle?.trim() || STANDARD_APP_NAME)

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

  return { einstellung, isLoaded, appName, fetchEinstellung }
})
