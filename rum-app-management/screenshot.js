const puppeteer = require('puppeteer');
const path = require('path');

async function takeScreenshots() {
  const browser = await puppeteer.launch({ 
    headless: 'new',
    args: ['--no-sandbox', '--disable-setuid-sandbox']
  });
  const page = await browser.newPage();
  
  await page.setViewport({ width: 1440, height: 900 });
  
  const htmlPath = `file://${path.join(__dirname, 'rum.html')}`;
  await page.goto(htmlPath, { waitUntil: 'networkidle0' });
  
  // 01 - 应用列表页
  await page.screenshot({ path: 'screenshots/01-app-list.png', fullPage: false });
  console.log('截图完成: 01-app-list.png');
  
  // 02 - 新建应用弹窗
  await page.click('button[onclick="showCreateModal()"]');
  await page.waitForSelector('#create-modal:not(.hidden)', { timeout: 3000 });
  await page.screenshot({ path: 'screenshots/02-create-app-modal.png', fullPage: false });
  console.log('截图完成: 02-create-app-modal.png');
  await page.click('#create-modal .modal-overlay');
  await new Promise(r => setTimeout(r, 300));
  
  // 03 - 应用配置页 - 基本信息
  await page.click('tr[onclick*="showAppConfig"]');
  await page.waitForSelector('#app-config-view:not(.hidden)', { timeout: 3000 });
  await page.screenshot({ path: 'screenshots/03-config-basic.png', fullPage: false });
  console.log('截图完成: 03-config-basic.png');
  
  // 04 - SDK 接入
  await page.evaluate(() => {
    document.querySelectorAll('#config-tabs button')[1].click();
  });
  await new Promise(r => setTimeout(r, 300));
  await page.screenshot({ path: 'screenshots/04-config-sdk.png', fullPage: false });
  console.log('截图完成: 04-config-sdk.png');
  
  // 05 - 数据采集
  await page.evaluate(() => {
    document.querySelectorAll('#config-tabs button')[2].click();
  });
  await new Promise(r => setTimeout(r, 300));
  await page.screenshot({ path: 'screenshots/05-config-collection.png', fullPage: false });
  console.log('截图完成: 05-config-collection.png');
  
  // 06 - 页面规则
  await page.evaluate(() => {
    document.querySelectorAll('#config-tabs button')[3].click();
  });
  await new Promise(r => setTimeout(r, 300));
  await page.screenshot({ path: 'screenshots/06-config-rules.png', fullPage: false });
  console.log('截图完成: 06-config-rules.png');
  
  // 07 - 阈值告警
  await page.evaluate(() => {
    document.querySelectorAll('#config-tabs button')[4].click();
  });
  await new Promise(r => setTimeout(r, 300));
  await page.screenshot({ path: 'screenshots/07-config-threshold.png', fullPage: false });
  console.log('截图完成: 07-config-threshold.png');
  
  // 08 - 体验评分
  await page.evaluate(() => {
    document.querySelectorAll('#config-tabs button')[5].click();
  });
  await new Promise(r => setTimeout(r, 300));
  await page.screenshot({ path: 'screenshots/08-config-scoring.png', fullPage: false });
  console.log('截图完成: 08-config-scoring.png');
  
  // 09 - 高级设置
  await page.evaluate(() => {
    document.querySelectorAll('#config-tabs button')[6].click();
  });
  await new Promise(r => setTimeout(r, 300));
  await page.screenshot({ path: 'screenshots/09-config-advanced.png', fullPage: false });
  console.log('截图完成: 09-config-advanced.png');
  
  // 10 - 删除确认弹窗
  await page.evaluate(() => {
    document.getElementById('delete-modal').classList.remove('hidden');
  });
  await new Promise(r => setTimeout(r, 300));
  await page.screenshot({ path: 'screenshots/10-delete-confirm.png', fullPage: false });
  console.log('截图完成: 10-delete-confirm.png');
  
  await browser.close();
  console.log('\n所有截图完成!');
}

takeScreenshots().catch(console.error);
