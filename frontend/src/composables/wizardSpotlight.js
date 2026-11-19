import { ref } from 'vue'

// Shared state for pointing at UI elements from the Einführungswizard.
//
// - markierung: a pulsing ring (with a short label) around an element while the wizard
//   dialog is open, e.g. the menu entry where a step's task can be found.
// - spotlight:  after leaving the wizard via a step's action, the page is dimmed except for
//   the element to use next (e.g. the "Neu" button), with an explanation next to it.
//
// Elements are found via `data-tour="…"` attributes; `ziel` may be a single name or a list
// (the first one present on the page wins).
const markierung = ref(null) // { ziel, label }
const spotlight = ref(null) // { ziel, title, text }

export const tourSelektor = (ziel) =>
  (Array.isArray(ziel) ? ziel : [ziel]).map((z) => `[data-tour="${z}"]`)

export const useWizardSpotlight = () => {
  const markieren = (m) => {
    markierung.value = m ? { ...m } : null
  }
  const zeigen = (s) => {
    spotlight.value = s ? { ...s } : null
  }
  const schliessen = () => {
    spotlight.value = null
  }

  return { markierung, spotlight, markieren, zeigen, schliessen }
}
