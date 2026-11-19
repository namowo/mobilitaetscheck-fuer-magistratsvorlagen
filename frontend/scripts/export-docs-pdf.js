/* eslint-env node */
// Exports the MkDocs print page to a PDF.
// Usage: node scripts/export-docs-pdf.js <url> <pdfPath> <title>
// Uses CHROME_BIN if set, otherwise the locally installed Google Chrome
// (puppeteer's own Chrome download is disabled in .puppeteerrc.cjs).
import puppeteer from 'puppeteer'

const [url, pdfPath, title] = process.argv.slice(2)

console.log('Saving', url, 'to', pdfPath)

const headerHtml = `
 <div style="font-size: 10px; padding-right: 1em; text-align: right; width: 100%;">
     <span>${title}</span>
  <span class="pageNumber"></span> / <span class="totalPages"></span>
 </div>`

const footerHtml = ` `

const browser = await puppeteer.launch({
  headless: true,
  ...(process.env.CHROME_BIN
    ? { executablePath: process.env.CHROME_BIN }
    : { channel: 'chrome' }),
  args: ['--no-sandbox', '--headless', '--disable-gpu', '--disable-dev-shm-usage']
})

try {
  const page = await browser.newPage()
  await page.goto(url, { waitUntil: 'networkidle2' })
  await page.pdf({
    path: pdfPath,
    format: 'A4',
    displayHeaderFooter: true,
    printBackground: true,
    landscape: false,
    headerTemplate: headerHtml,
    footerTemplate: footerHtml,
    scale: 1,
    margin: { top: 80, bottom: 80, left: 30, right: 30 }
  })
} finally {
  await browser.close()
}
