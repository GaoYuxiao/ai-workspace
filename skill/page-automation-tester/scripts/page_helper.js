/**
 * 页面自动化测试辅助脚本
 * 注入到目标页面，提供快速元素定位和批量操作能力
 * 
 * 使用方法：
 * 1. 在测试开始时注入此脚本：evaluate_script("() => { /* 脚本内容 */ }")
 * 2. 使用 window.__testHelper 提供的API进行快速操作
 */

(function() {
  'use strict';

  // 避免重复注入
  if (window.__testHelper) {
    console.log('[TestHelper] 辅助脚本已存在，跳过重复注入');
    return;
  }

  /**
   * 元素定位器 - 快速查找元素
   */
  const ElementFinder = {
    /**
     * 通过文本查找元素（支持模糊匹配）
     * @param {string} text - 要查找的文本
     * @param {string} tagName - 元素标签名（可选）
     * @returns {Array} 匹配的元素数组
     */
    findByText(text, tagName = null) {
      const walker = document.createTreeWalker(
        document.body,
        NodeFilter.SHOW_TEXT,
        null
      );
      
      const results = [];
      let node;
      
      while (node = walker.nextNode()) {
        if (node.textContent.includes(text)) {
          const element = node.parentElement;
          if (!tagName || element.tagName.toLowerCase() === tagName.toLowerCase()) {
            // 生成唯一标识
            const uid = this._generateUID(element);
            results.push({
              uid: uid,
              element: element,
              text: node.textContent.trim(),
              tagName: element.tagName,
              role: element.getAttribute('role') || '',
              name: element.getAttribute('name') || element.getAttribute('id') || '',
              className: element.className || ''
            });
          }
        }
      }
      
      return results;
    },

    /**
     * 通过角色（role）查找元素
     * @param {string} role - ARIA角色
     * @returns {Array} 匹配的元素数组
     */
    findByRole(role) {
      const elements = document.querySelectorAll(`[role="${role}"]`);
      return Array.from(elements).map(el => ({
        uid: this._generateUID(el),
        element: el,
        role: role,
        text: el.textContent?.trim() || '',
        tagName: el.tagName
      }));
    },

    /**
     * 通过标签名和文本查找
     * @param {string} tagName - 标签名（如 'button', 'input'）
     * @param {string} text - 文本内容（可选）
     * @returns {Array} 匹配的元素数组
     */
    findByTagAndText(tagName, text = null) {
      const elements = document.querySelectorAll(tagName);
      const results = [];
      
      Array.from(elements).forEach(el => {
        if (!text || el.textContent?.includes(text) || el.value?.includes(text)) {
          results.push({
            uid: this._generateUID(el),
            element: el,
            tagName: tagName,
            text: el.textContent?.trim() || el.value || '',
            type: el.type || '',
            name: el.name || el.id || ''
          });
        }
      });
      
      return results;
    },

    /**
     * 通过选择器查找元素
     * @param {string} selector - CSS选择器
     * @returns {Array} 匹配的元素数组
     */
    findBySelector(selector) {
      try {
        const elements = document.querySelectorAll(selector);
        return Array.from(elements).map(el => ({
          uid: this._generateUID(el),
          element: el,
          selector: selector,
          text: el.textContent?.trim() || el.value || ''
        }));
      } catch (e) {
        console.error('[TestHelper] 选择器错误:', e);
        return [];
      }
    },

    /**
     * 生成元素唯一标识
     * @private
     */
    _generateUID(element) {
      if (element.__testUID) {
        return element.__testUID;
      }
      
      // 尝试使用id
      if (element.id) {
        element.__testUID = element.id;
        return element.id;
      }
      
      // 生成基于位置的唯一ID
      const path = [];
      let current = element;
      while (current && current !== document.body) {
        let index = 0;
        let sibling = current.previousElementSibling;
        while (sibling) {
          index++;
          sibling = sibling.previousElementSibling;
        }
        path.unshift(`${current.tagName.toLowerCase()}:nth-child(${index + 1})`);
        current = current.parentElement;
      }
      
      const uid = `test_${path.join('>')}_${Date.now()}`;
      element.__testUID = uid;
      return uid;
    }
  };

  /**
   * 批量操作执行器
   */
  const BatchExecutor = {
    /**
     * 批量执行操作
     * @param {Array} operations - 操作数组
     * @returns {Object} 执行结果
     */
    async execute(operations) {
      const results = [];
      
      for (const op of operations) {
        try {
          const result = await this._executeOperation(op);
          results.push({
            operation: op,
            success: true,
            result: result
          });
        } catch (error) {
          results.push({
            operation: op,
            success: false,
            error: error.message
          });
        }
      }
      
      return {
        total: operations.length,
        success: results.filter(r => r.success).length,
        failed: results.filter(r => !r.success).length,
        results: results
      };
    },

    /**
     * 执行单个操作
     * @private
     */
    async _executeOperation(op) {
      const { action, target, value, options = {} } = op;
      
      // 查找元素
      let element = null;
      if (target) {
        if (target.startsWith('test_') || document.getElementById(target)) {
          element = document.getElementById(target) || 
                   document.querySelector(`[data-test-uid="${target}"]`);
        } else {
          // 通过文本查找
          const found = ElementFinder.findByText(target);
          if (found.length > 0) {
            element = found[0].element;
          }
        }
      }

      switch (action) {
        case 'click':
          if (!element) throw new Error(`找不到目标元素: ${target}`);
          element.click();
          return { action: 'click', target: target };
          
        case 'fill':
          if (!element) throw new Error(`找不到目标元素: ${target}`);
          element.value = value;
          element.dispatchEvent(new Event('input', { bubbles: true }));
          element.dispatchEvent(new Event('change', { bubbles: true }));
          return { action: 'fill', target: target, value: value };
          
        case 'wait':
          await new Promise(resolve => setTimeout(resolve, value || 1000));
          return { action: 'wait', duration: value };
          
        case 'waitForElement':
          const maxWait = options.timeout || 5000;
          const startTime = Date.now();
          while (Date.now() - startTime < maxWait) {
            const found = ElementFinder.findByText(target);
            if (found.length > 0) {
              return { action: 'waitForElement', target: target, found: true };
            }
            await new Promise(resolve => setTimeout(resolve, 100));
          }
          throw new Error(`等待元素超时: ${target}`);
          
        default:
          throw new Error(`不支持的操作: ${action}`);
      }
    }
  };

  /**
   * 快速验证器
   */
  const QuickValidator = {
    /**
     * 批量验证
     * @param {Array} validations - 验证规则数组
     * @returns {Object} 验证结果
     */
    validate(validations) {
      const results = [];
      
      for (const validation of validations) {
        try {
          const result = this._validate(validation);
          results.push({
            ...validation,
            passed: result.passed,
            actualValue: result.actualValue,
            message: result.message
          });
        } catch (error) {
          results.push({
            ...validation,
            passed: false,
            error: error.message
          });
        }
      }
      
      return {
        total: validations.length,
        passed: results.filter(r => r.passed).length,
        failed: results.filter(r => !r.passed).length,
        results: results
      };
    },

    /**
     * 执行单个验证
     * @private
     */
    _validate(validation) {
      const { type, target, expectedValue } = validation;
      
      switch (type) {
        case 'element_exists':
          const found = ElementFinder.findByText(target);
          return {
            passed: found.length > 0,
            actualValue: found.length > 0 ? '存在' : '不存在',
            message: found.length > 0 ? '元素存在' : '元素不存在'
          };
          
        case 'text_contains':
          const elements = ElementFinder.findByText(target);
          if (elements.length === 0) {
            return { passed: false, actualValue: null, message: '目标元素不存在' };
          }
          const text = elements[0].element.textContent || '';
          const contains = text.includes(expectedValue);
          return {
            passed: contains,
            actualValue: text,
            message: contains ? '文本包含期望值' : `文本不包含期望值，实际: ${text}`
          };
          
        case 'url_contains':
          const url = window.location.href;
          const urlContains = url.includes(expectedValue);
          return {
            passed: urlContains,
            actualValue: url,
            message: urlContains ? 'URL包含期望值' : `URL不包含期望值，实际: ${url}`
          };
          
        case 'url_equals':
          const currentUrl = window.location.href;
          const urlEquals = currentUrl === expectedValue;
          return {
            passed: urlEquals,
            actualValue: currentUrl,
            message: urlEquals ? 'URL匹配' : `URL不匹配，实际: ${currentUrl}`
          };
          
        default:
          throw new Error(`不支持的验证类型: ${type}`);
      }
    }
  };

  /**
   * 元素缓存管理器
   */
  const ElementCache = {
    cache: new Map(),
    
    /**
     * 缓存元素
     */
    cacheElement(key, element) {
      this.cache.set(key, {
        element: element,
        uid: element.__testUID || ElementFinder._generateUID(element),
        timestamp: Date.now()
      });
    },
    
    /**
     * 获取缓存的元素
     */
    getCached(key) {
      const cached = this.cache.get(key);
      if (cached && cached.element.isConnected) {
        return cached;
      }
      // 元素已不在DOM中，清除缓存
      if (cached) {
        this.cache.delete(key);
      }
      return null;
    },
    
    /**
     * 清除缓存
     */
    clear() {
      this.cache.clear();
    }
  };

  // 暴露全局API
  window.__testHelper = {
    find: ElementFinder,
    batch: BatchExecutor,
    validate: QuickValidator,
    cache: ElementCache,
    
    /**
     * 快速查找并返回元素信息（用于生成测试用例）
     */
    quickFind(description) {
      // 尝试多种方式查找
      const results = {
        byText: ElementFinder.findByText(description),
        byRole: description.includes('按钮') ? ElementFinder.findByRole('button') : [],
        byTag: description.includes('输入') ? ElementFinder.findByTagAndText('input') : 
               description.includes('按钮') ? ElementFinder.findByTagAndText('button') : []
      };
      
      // 合并结果
      const allResults = [
        ...results.byText,
        ...results.byRole,
        ...results.byTag
      ];
      
      // 去重
      const uniqueResults = Array.from(
        new Map(allResults.map(r => [r.uid, r])).values()
      );
      
      return uniqueResults;
    },
    
    /**
     * 获取页面所有可交互元素（类似snapshot但更快）
     */
    getInteractiveElements() {
      const interactive = [];
      const selectors = [
        'button', 'a', 'input', 'select', 'textarea',
        '[role="button"]', '[role="link"]', '[onclick]',
        '[tabindex]:not([tabindex="-1"])'
      ];
      
      selectors.forEach(selector => {
        const elements = document.querySelectorAll(selector);
        Array.from(elements).forEach(el => {
          if (el.offsetParent !== null) { // 可见元素
            interactive.push({
              uid: ElementFinder._generateUID(el),
              element: el,
              tagName: el.tagName,
              text: el.textContent?.trim() || el.value || el.placeholder || '',
              role: el.getAttribute('role') || '',
              type: el.type || '',
              name: el.name || el.id || ''
            });
          }
        });
      });
      
      return interactive;
    }
  };

  console.log('[TestHelper] 页面辅助脚本已注入');
  console.log('[TestHelper] 使用 window.__testHelper 访问API');
})();


