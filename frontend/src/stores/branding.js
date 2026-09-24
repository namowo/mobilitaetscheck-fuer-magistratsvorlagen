import { ref } from 'vue'
import { defineStore } from 'pinia'
import { useFavicon } from '@vueuse/core'
import { apiClient } from '@/services/axios'

export const useBrandingStore = defineStore('branding', () => {
  const slots = ref({})
  const menueleisteLogos = ref([])
  const footerLogos = ref([])
  const loginLogos = ref([])
  const isLoaded = ref(false)
  const favicon = useFavicon()

  async function fetchBranding() {
    try {
      const [slotsRes, menueleisteRes, footerRes, loginRes] = await Promise.all([
        apiClient.get('/branding'),
        apiClient.get('/branding/logo-listen/menueleiste'),
        apiClient.get('/branding/logo-listen/footer'),
        apiClient.get('/branding/logo-listen/login')
      ])
      slots.value = Object.fromEntries(slotsRes.data.map((s) => [s.slot, s]))
      menueleisteLogos.value = menueleisteRes.data
      footerLogos.value = footerRes.data
      loginLogos.value = loginRes.data
      applyFavicon()
    } catch {
      slots.value = {}
      menueleisteLogos.value = []
      footerLogos.value = []
      loginLogos.value = []
    } finally {
      isLoaded.value = true
    }
  }

  function url(slot) {
    return slots.value[slot]?.asset?.url || null
  }

  function link(slot) {
    return slots.value[slot]?.link || null
  }

  function applyFavicon() {
    const faviconUrl = url('favicon')
    if (!faviconUrl) {
      try {
        localStorage.removeItem('brandingFaviconUrl')
      } catch {
        // localStorage unavailable, ignore
      }
      return
    }
    favicon.value = faviconUrl
    try {
      localStorage.setItem('brandingFaviconUrl', faviconUrl)
    } catch {
      // localStorage unavailable, ignore
    }
  }

  return {
    slots,
    menueleisteLogos,
    footerLogos,
    loginLogos,
    isLoaded,
    fetchBranding,
    url,
    link
  }
})
