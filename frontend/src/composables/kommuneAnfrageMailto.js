import { ref, computed } from 'vue'
import { apiClient } from '@/services/axios'
import { useEinstellungStore } from '@/stores/einstellung'
import { storeToRefs } from 'pinia'

export function useKommuneAnfrageMailto(rolle) {
  const { einstellung } = storeToRefs(useEinstellungStore())
  const kontaktEmail = computed(() => einstellung.value.kontaktEmail || '')

  const betreff = ref('')
  const inhalt = ref('')

  const fetchVorlage = async () => {
    try {
      const res = await apiClient.get(`/public/kommune-anfrage-vorlage/${rolle}`)
      betreff.value = res.data.betreff
      inhalt.value = res.data.inhalt
    } catch {
      betreff.value = ''
      inhalt.value = ''
    }
  }

  const mailtoHref = computed(() => {
    const subject = encodeURIComponent(betreff.value)
    const body = encodeURIComponent(inhalt.value)
    return `mailto:${kontaktEmail.value}?subject=${subject}&body=${body}`
  })

  return { kontaktEmail, mailtoHref, fetchVorlage }
}
