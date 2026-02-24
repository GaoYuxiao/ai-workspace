#!/bin/bash

# Script to capture screenshots of RUM application management page
# This script uses playwright/puppeteer or similar tool to automate browser screenshots

SCREENSHOTS_DIR="/Users/yuxiaogao/cursor/日志AI特性/rum-app-management/screenshots"
HTML_FILE="file:///Users/yuxiaogao/cursor/日志AI特性/rum-app-management/rum.html"

echo "=== RUM Application Management Screenshot Capture Script ==="
echo "Screenshots directory: $SCREENSHOTS_DIR"
echo "HTML file: $HTML_FILE"
echo ""
echo "To capture screenshots, you can:"
echo ""
echo "Option 1 - Manual Capture:"
echo "1. Open the HTML file in your browser"
echo "2. Set browser window to 1440x900"
echo "3. Follow these steps:"
echo ""
echo "   01-app-list.png: Capture the main application list page"
echo "   02-create-app-modal.png: Click '新建应用' button, then capture"
echo "   03-config-basic.png: Click on '官网首页' row, capture '基本信息' tab"
echo "   04-config-sdk.png: Click 'SDK 接入' tab, capture"
echo "   05-config-collection.png: Click '数据采集' tab, capture"
echo "   06-config-rules.png: Click '页面规则' tab, capture"
echo "   07-config-threshold.png: Click '阈值告警' tab, capture"
echo "   08-config-scoring.png: Click '体验评分' tab, capture"
echo "   09-config-advanced.png: Click '高级设置' tab, capture"
echo ""
echo "Option 2 - Automated Capture (requires Node.js and Playwright):"
echo "Run: node capture-screenshots.js"
echo ""
