const puppeteer = require('puppeteer');
var args = process.argv.slice(2);
var url = args[0];
var pdfPath = args[1];
var title = args[2];

console.log('Saving', url, 'to', pdfPath);

headerHtml = `
 <div style="font-size: 10px; padding-right: 1em; text-align: right; width: 100%;">
     <span>${title}</span>
  <span class="pageNumber"></span> / <span class="totalPages"></span>
 </div>`;

footerHtml = ` `;

(async() => {
    const browser = await puppeteer.launch({
        headless: true,
        executablePath: process.env.CHROME_BIN || null,
        args: ['--no-sandbox', '--headless', '--disable-gpu', '--disable-dev-shm-usage']
    });

    const page = await browser.newPage();
    await page.goto(url, { waitUntil: 'networkidle2' });
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
    });

    await browser.close();
})();
