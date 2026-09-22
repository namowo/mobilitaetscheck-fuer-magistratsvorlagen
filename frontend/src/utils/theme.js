const SHADE_KEYS = [50, 100, 200, 300, 400, 500, 600, 700, 800, 900, 950]

// Target lightness (0-100) for each shade, tuned to resemble PrimeVue's Aura preset scales.
const SHADE_LIGHTNESS = {
  50: 95,
  100: 90,
  200: 80,
  300: 70,
  400: 60,
  500: 45,
  600: 35,
  700: 27,
  800: 19,
  900: 12,
  950: 7
}

function hexToRgb(hex) {
  const match = /^#?([0-9a-f]{6})$/i.exec(hex)
  if (!match) return null
  const int = parseInt(match[1], 16)
  return { r: (int >> 16) & 255, g: (int >> 8) & 255, b: int & 255 }
}

function rgbToHsl({ r, g, b }) {
  r /= 255
  g /= 255
  b /= 255
  const max = Math.max(r, g, b)
  const min = Math.min(r, g, b)
  const l = (max + min) / 2
  let h = 0
  let s = 0
  if (max !== min) {
    const d = max - min
    s = l > 0.5 ? d / (2 - max - min) : d / (max + min)
    switch (max) {
      case r:
        h = (g - b) / d + (g < b ? 6 : 0)
        break
      case g:
        h = (b - r) / d + 2
        break
      default:
        h = (r - g) / d + 4
    }
    h /= 6
  }
  return { h: h * 360, s: s * 100, l: l * 100 }
}

function hslToRgb({ h, s, l }) {
  h /= 360
  s /= 100
  l /= 100
  if (s === 0) {
    const v = Math.round(l * 255)
    return { r: v, g: v, b: v }
  }
  const q = l < 0.5 ? l * (1 + s) : l + s - l * s
  const p = 2 * l - q
  const hueToRgb = (t) => {
    if (t < 0) t += 1
    if (t > 1) t -= 1
    if (t < 1 / 6) return p + (q - p) * 6 * t
    if (t < 1 / 2) return q
    if (t < 2 / 3) return p + (q - p) * (2 / 3 - t) * 6
    return p
  }
  return {
    r: Math.round(hueToRgb(h + 1 / 3) * 255),
    g: Math.round(hueToRgb(h) * 255),
    b: Math.round(hueToRgb(h - 1 / 3) * 255)
  }
}

function rgbToHex({ r, g, b }) {
  const toHex = (v) => Math.max(0, Math.min(255, v)).toString(16).padStart(2, '0')
  return `#${toHex(r)}${toHex(g)}${toHex(b)}`
}

/**
 * Generates a PrimeVue-style 50-950 shade scale (hex + RGB triple) from a base hex color,
 * by keeping the base color's hue/saturation and interpolating lightness per shade.
 */
export function generateShades(baseHex) {
  const rgb = hexToRgb(baseHex)
  if (!rgb) return null
  const { h, s } = rgbToHsl(rgb)
  const shades = {}
  for (const key of SHADE_KEYS) {
    const shadeRgb = hslToRgb({ h, s, l: SHADE_LIGHTNESS[key] })
    shades[key] = { hex: rgbToHex(shadeRgb), rgb: shadeRgb }
  }
  return shades
}

/**
 * Applies a base theme color to the document by setting the --p-primary-* and --primary-*
 * CSS custom properties on :root, mirroring the shades defined in main.css. Also sets
 * --primary-base to the exact input color (unshaded), for areas like the header/footer
 * that should reflect the admin's chosen color as-is rather than a derived shade.
 */
export function applyThemeColor(baseHex) {
  const shades = generateShades(baseHex)
  if (!shades) return
  const root = document.documentElement.style
  for (const key of SHADE_KEYS) {
    const { hex, rgb } = shades[key]
    root.setProperty(`--p-primary-${key}`, hex)
    root.setProperty(`--primary-${key}`, `${rgb.r} ${rgb.g} ${rgb.b}`)
  }
  const baseRgb = hexToRgb(baseHex)
  if (baseRgb) {
    root.setProperty('--primary-base', `${baseRgb.r} ${baseRgb.g} ${baseRgb.b}`)
  }
}
