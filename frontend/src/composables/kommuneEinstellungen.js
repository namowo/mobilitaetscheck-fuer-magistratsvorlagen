import { ref } from 'vue'
import { apiClient } from '@/services/axios'
import { useAuthStore } from '@/stores/auth'

const API = '/einstellungen/fremde-eintraege'

// Modulweiter Zustand: wird einmal geladen und von allen Komponenten geteilt
const werte = ref({
  fremdeTagsAnzeigen: true,
  fremdeIndikatorenAnzeigen: true,
  fremdeTextbausteineAnzeigen: true,
  inhalteTeilen: true
})
const geladen = ref(false)
// Für welche Kommune geladen wurde (Wechsel z. B. nach erneutem Login)
let geladenFuerGemeinde = null
let ladeVorgang = null

/**
 * Kommunale Einstellungen zum Austausch von Tags, Indikatoren und Textbausteinen.
 */
export const useKommuneEinstellungen = () => {
  const authStore = useAuthStore()

  const laden = async ({ neu = false } = {}) => {
    if (geladen.value && !neu && geladenFuerGemeinde === authStore.gemeindeId) return werte.value
    ladeVorgang ??= apiClient
      .get(API)
      .then(({ data }) => {
        werte.value = data
        geladen.value = true
        geladenFuerGemeinde = authStore.gemeindeId
        return data
      })
      .finally(() => {
        ladeVorgang = null
      })
    return ladeVorgang
  }

  const speichern = async (aenderung) => {
    const { data } = await apiClient.patch(API, aenderung)
    werte.value = data
    return data
  }

  return { werte, geladen, laden, speichern }
}
