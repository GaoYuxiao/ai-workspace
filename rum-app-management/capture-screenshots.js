// Automated screenshot capture script using Playwright
// Install: npm install playwright
// Run: node capture-screenshots.js

const { chromium } = require('playwright');
const path = require('path');
const fs = require('fs');

async function captureScreenshots() {
  const screenshotsDir = path.join(__dirname, 'screenshots');
  const htmlFile = `file://${path.join(__dirname, 'rum.html')}`;
  
  // Ensure screenshots directory exists
  if (!fs.existsSync(screenshotsDir)) {
    fs.mkdirSync(screenshotsDir);
  }
  
  console.log('Launching browser...');
  const browser = await chromium.launch({ headless: false });
  const context = await browser.newContext({
    viewport: { width: 1440, height: 900 }
  });
  const page = await context.newPage();
  
  try {
    console.log('Navigating to RUM application management page...');
    await page.goto(htmlFile);
    await page.waitForLoadState('networkidle');
    await page.waitForTimeout(1000);
    
    // 01. Main application list page
    console.log('Capturing 01-app-list.png...');
    await page.screenshot({ 
      path: path.join(screenshotsDir, '01-app-list.png'),
      fullPage: false
    });
    
    // 02. Create app modal
    console.log('Capturing 02-create-app-modal.png...');
    await page.click('button:has-text("新建应用")');
    await page.waitForTimeout(500);
    await page.screenshot({ 
      path: path.join(screenshotsDir, '02-create-app-modal.png'),
      fullPage: false
    });
    
    // Close modal
    await page.click('.bk-dialog-header .bk-dialog-close, .bk-modal-close, button:has-text("取消")');
    await page.waitForTimeout(500);
    
    // 03. Click on application row to enter config view (基本信息)
    console.log('Capturing 03-config-basic.png...');
    await page.click('.app-list-table tbody tr:first-child');
    await page.waitForTimeout(1000);
    await page.screenshot({ 
      path: path.join(screenshotsDir, '03-config-basic.png'),
      fullPage: false
    });
    
    // 04. SDK 接入 tab
    console.log('Capturing 04-config-sdk.png...');
    await page.click('.bk-tab-label:has-text("SDK 接入")');
    await page.waitForTimeout(500);
    await page.screenshot({ 
      path: path.join(screenshotsDir, '04-config-sdk.png'),
      fullPage: false
    });
    
    // 05. 数据采集 tab
    console.log('Capturing 05-config-collection.png...');
    await page.click('.bk-tab-label:has-text("数据采集")');
    await page.waitForTimeout(500);
    await page.screenshot({ 
      path: path.join(screenshotsDir, '05-config-collection.png'),
      fullPage: false
    });
    
    // 06. 页面规则 tab
    console.log('Capturing 06-config-rules.png...');
    await page.click('.bk-tab-label:has-text("页面规则")');
    await page.waitForTimeout(500);
    await page.screenshot({ 
      path: path.join(screenshotsDir, '06-config-rules.png'),
      fullPage: false
    });
    
    // 07. 阈值告警 tab
    console.log('Capturing 07-config-threshold.png...');
    await page.click('.bk-tab-label:has-text("阈值告警")');
    await page.waitForTimeout(500);
    await page.screenshot({ 
      path: path.join(screenshotsDir, '07-config-threshold.png'),
      fullPage: false
    });
    
    // 08. 体验评分 tab
    console.log('Capturing 08-config-scoring.png...');
    await page.click('.bk-tab-label:has-text("体验评分")');
    await page.waitForTimeout(500);
    await page.screenshot({ 
      path: path.join(screenshotsDir, '08-config-scoring.png'),
      fullPage: false
    });
    
    // 09. 高级设置 tab
    console.log('Capturing 09-config-advanced.png...');
    await page.click('.bk-tab-label:has-text("高级设置")');
    await page.waitForTimeout(500);
    await page.screenshot({ 
      path: path.join(screenshotsDir, '09-config-advanced.png'),
      fullPage: false
    });
    
    console.log('\n✅ All screenshots captured successfully!');
    console.log(`Screenshots saved to: ${screenshotsDir}`);
    
  } catch (error) {
    console.error('Error capturing screenshots:', error);
  } finally {
    await browser.close();
  }
}

captureScreenshots();
