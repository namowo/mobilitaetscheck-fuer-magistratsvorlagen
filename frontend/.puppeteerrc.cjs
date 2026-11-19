/* eslint-env node */
// puppeteer is only used by `npm run export-pdf` (docs PDF). Skip its ~170 MB
// Chrome download so `npm ci` in Docker, CI and deploy stays lean; the export
// script uses the installed Google Chrome or CHROME_BIN instead.
module.exports = {
  skipDownload: true
}
