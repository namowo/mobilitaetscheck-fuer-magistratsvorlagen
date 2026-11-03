import { ref } from 'vue'
import { apiClient } from '@/services/axios'

// Shared state: has the current Kommune defined its own Leitziel-Sets?
const hatEigeneZielSets = ref(true)

export const useLeitzieleStatus = () => {
  const pruefe = async () => {
    try {
      const res = await apiClient.get('/einstellungen/mobilitaetscheck/ziel-set/hat-eigene')
      hatEigeneZielSets.value = res.data.hatEigene
    } catch {
      hatEigeneZielSets.value = true
    }
  }
  return { hatEigeneZielSets, pruefe }
}
