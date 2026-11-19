// Wandelt HTML (z. B. aus dem Editor) in reinen Text um – für Suche und kompakte Vorschauen.
export const htmlZuText = (html) => {
  if (!html) return ''
  const doc = new DOMParser().parseFromString(html, 'text/html')
  // Blockelemente durch Leerzeichen trennen, damit Wörter nicht zusammenkleben
  doc.querySelectorAll('p, li, br, h1, h2, h3, blockquote').forEach((el) => el.append(' '))
  return (doc.body.textContent ?? '').replace(/\s+/g, ' ').trim()
}
