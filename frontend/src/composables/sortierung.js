import { computed, ref } from 'vue'
import { useAuthStore } from '@/stores/auth'
import { useKommuneEinstellungen } from '@/composables/kommuneEinstellungen'

// Gemeinsame Sortierung und Filter für Tags, Textbausteine, Indikatoren und Gebiete
export const sortierOptionen = [
  { label: 'Name (A–Z)', value: 'name-auf' },
  { label: 'Name (Z–A)', value: 'name-ab' },
  { label: 'Neueste zuerst', value: 'neu' },
  { label: 'Älteste zuerst', value: 'alt' },
  { label: 'Sichtbarkeit', value: 'sichtbarkeit' }
]

export const sichtbarkeitOptionen = [
  { label: 'Alle', value: 'alle' },
  { label: 'Sichtbar', value: 'sichtbar' },
  { label: 'Privat', value: 'privat' },
  { label: 'Andere Kommunen', value: 'andere' }
]

/**
 * @param {object} [optionen]
 * @param {(item: object) => string} [optionen.anzeigename] – Text für Suche und Sortierung
 * @param {Record<string, {label: string, test: (item: object) => boolean}>} [optionen.zusatzFilter]
 *   – zusätzliche Ein/Aus-Filter, die im Filter-Drawer als Schalter erscheinen
 */
export const useSortierung = ({
  anzeigename = (item) => item.name ?? '',
  zusatzFilter = {}
} = {}) => {
  const authStore = useAuthStore()
  const suche = ref('')
  const sortierung = ref('name-auf')
  const sichtbarkeit = ref('alle')
  const tagIds = ref([])
  const zusatz = ref(Object.fromEntries(Object.keys(zusatzFilter).map((key) => [key, false])))
  const zusatzOptionen = Object.entries(zusatzFilter).map(([key, { label }]) => ({ key, label }))

  const { werte: kommune } = useKommuneEinstellungen()

  const istAndere = (item) => item.gemeindeId !== authStore.gemeindeId
  // Eigener Eintrag ist nur geteilt, wenn er sichtbar ist und die Kommune das Teilen erlaubt
  const istGeteilt = (item) => !item.gemeindespezifisch && kommune.value.inhalteTeilen

  // Eigene sichtbare, eigene private, dann Einträge anderer Kommunen
  const sichtbarkeitsRang = (item) => {
    if (istAndere(item)) return 2
    return istGeteilt(item) ? 0 : 1
  }

  const nachName = (a, b) =>
    anzeigename(a).localeCompare(anzeigename(b), 'de', { sensitivity: 'base' })

  // Neu/alt über die ID, da keine Zeitstempel vorliegen (IDs steigen beim Anlegen)
  const vergleicher = {
    'name-auf': nachName,
    'name-ab': (a, b) => nachName(b, a),
    neu: (a, b) => b.id - a.id,
    alt: (a, b) => a.id - b.id,
    sichtbarkeit: (a, b) => sichtbarkeitsRang(a) - sichtbarkeitsRang(b) || nachName(a, b)
  }

  const passtSichtbarkeit = {
    alle: () => true,
    sichtbar: (item) => !istAndere(item) && istGeteilt(item),
    privat: (item) => !istAndere(item) && !istGeteilt(item),
    andere: istAndere
  }

  const sortieren = (liste) => [...liste].sort(vergleicher[sortierung.value] ?? nachName)

  // Suche (Name und Tags), Filter und Sortierung in einem Schritt
  const anwenden = (liste) => {
    const query = suche.value.trim().toLowerCase()
    const filterSichtbarkeit = passtSichtbarkeit[sichtbarkeit.value] ?? passtSichtbarkeit.alle
    const gefiltert = liste.filter(
      (item) =>
        filterSichtbarkeit(item) &&
        Object.entries(zusatz.value).every(
          ([key, aktiv]) => !aktiv || zusatzFilter[key].test(item)
        ) &&
        (tagIds.value.length === 0 ||
          (item.tags ?? []).some((tag) => tagIds.value.includes(tag.id))) &&
        (!query ||
          anzeigename(item).toLowerCase().includes(query) ||
          (item.tags ?? []).some((tag) => tag.name.toLowerCase().includes(query)))
    )
    return sortieren(gefiltert)
  }

  // Anzahl aktiver Filter für das Badge am Filter-Button (Sortierung zählt nicht)
  const anzahlFilter = computed(
    () =>
      (sichtbarkeit.value !== 'alle' ? 1 : 0) +
      (tagIds.value.length > 0 ? 1 : 0) +
      Object.values(zusatz.value).filter(Boolean).length
  )

  const zuruecksetzen = () => {
    suche.value = ''
    sortierung.value = 'name-auf'
    sichtbarkeit.value = 'alle'
    tagIds.value = []
    for (const key of Object.keys(zusatz.value)) zusatz.value[key] = false
  }

  return {
    suche,
    sortierung,
    sichtbarkeit,
    tagIds,
    zusatz,
    zusatzOptionen,
    anzahlFilter,
    sortieren,
    anwenden,
    zuruecksetzen
  }
}
