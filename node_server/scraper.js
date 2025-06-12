const puppeteer = require('puppeteer-core');


(async () => {
  const browser = await puppeteer.launch({
    executablePath: 'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe', // <-- your Chrome path here
    headless: false // set to true if you want headless mode
  });

  const page = await browser.newPage();

  await page.goto('https://www.sharesansar.com/company/nmb');

  await page.setViewport({ width: 1080, height: 1024 });

    // Wait for the element to appear in the DOM and be visible
    await page.waitForSelector('#cpricehistory', { visible: true });

    // Then click it
    await page.click('#cpricehistory');

    await page.select('select[name="myTableCPriceHistory_length"]', '50');

    
  await browser.close();
})();
