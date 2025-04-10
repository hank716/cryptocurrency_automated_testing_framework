---
marp: true
theme: default
paginate: true
backgroundColor: #fff
---

# 加密貨幣自動化測試框架
## CoinMarketCap Automation QA Engineer 面試專案

---

# 專案概述

- **目標**：開發全面的加密貨幣自動化測試框架
- **核心模組**：
  - API 測試模組
  - Web UI 測試模組
  - 性能測試模組
  - CI/CD 整合
- **技術棧**：Python, pytest, Selenium, Locust, GitHub Actions

---

# 為什麼選擇這個專案？

- **完全符合職位要求**
  - 自動化測試框架開發
  - API 測試和 Web UI 測試
  - 性能測試和壓力測試
  - CI/CD 整合

- **展示全面技能**
  - 編程能力
  - 測試設計
  - 架構設計
  - DevOps 實踐

---

# API 測試模組

- **核心功能**
  - 加密貨幣 API 功能測試
  - 交易所 API 功能測試
  - API 性能監控
  - 數據驗證和一致性檢查

- **技術亮點**
  - 數據驅動測試
  - 自定義重試機制
  - 詳細的測試報告

---

# Web UI 測試模組

- **核心功能**
  - 頁面對象模型 (POM) 架構
  - 導航和搜索功能測試
  - 市場數據顯示測試
  - 跨瀏覽器兼容性測試

- **技術亮點**
  - 模塊化設計
  - 自動截圖和錯誤處理
  - 靈活的元素定位策略

---

# 性能測試模組

- **核心功能**
  - API 負載測試
  - Web 負載測試
  - 壓力測試
  - 穩定性測試

- **技術亮點**
  - 用戶行為模擬
  - 可配置的測試參數
  - 詳細的性能指標收集和分析

---

# CI/CD 整合

- **核心功能**
  - GitHub Actions 工作流配置
  - 自動化測試執行
  - 測試報告自動生成
  - 測試結果通知機制

- **技術亮點**
  - 多階段工作流
  - 條件執行策略
  - 自動化部署

---

# 代碼展示：API 測試

```python
@pytest.mark.api
class TestCryptocurrency:
    """加密貨幣 API 測試類"""
    
    @pytest.mark.parametrize("limit", [10, 50, 100])
    def test_get_cryptocurrency_listings(self, api_client, limit):
        """測試獲取加密貨幣列表"""
        response = api_client.get_cryptocurrency_listings(limit=limit)
        
        # 驗證響應
        assert response.status_code == 200
        assert "data" in response.json()
        assert len(response.json()["data"]) <= limit
```

---

# 代碼展示：Web UI 測試

```python
@pytest.mark.web
class TestNavigation:
    """導航測試類"""
    
    @pytest.mark.smoke
    def test_homepage_navigation(self, driver, base_url):
        """測試首頁導航"""
        home_page = HomePage(driver)
        home_page.open(base_url)
        
        # 驗證頁面加載
        assert home_page.is_page_loaded()
        
        # 測試導航到加密貨幣頁面
        home_page.navigate_to_cryptocurrencies()
        assert "cryptocurrencies" in driver.current_url.lower()
```

---

# 代碼展示：性能測試

```python
class CryptoAPIUser(HttpUser):
    """加密貨幣 API 負載測試用戶"""
    
    wait_time = between(1, 5)
    
    @task(3)
    def get_cryptocurrency_listings(self):
        """獲取加密貨幣列表（高頻任務）"""
        params = {
            "limit": random.choice([10, 20, 50, 100]),
            "sort": random.choice(["market_cap", "volume_24h"]),
            "convert": random.choice(["USD", "EUR", "JPY"])
        }
        
        self.client.get("/v1/cryptocurrency/listings/latest", 
                        params=params, name="/v1/cryptocurrency/listings/latest")
```

---

# 代碼展示：CI/CD 配置

```yaml
jobs:
  api_tests:
    name: API 測試
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: 設置 Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.10'
      - name: 安裝依賴
        run: pip install -r requirements.txt
      - name: 運行 API 測試
        run: pytest api_tests/ -v --html=reports/api_test_report.html
```

---

# 專案特色與優勢

- **全面覆蓋**：API、Web UI 和性能測試
- **高度可擴展**：模塊化設計，易於添加新功能
- **自動化程度高**：從測試執行到報告生成
- **易於維護**：良好的代碼結構和文檔
- **CI/CD 整合**：無縫集成到開發流程

---

# 技術挑戰與解決方案

- **挑戰**：處理動態變化的 UI 元素
- **解決方案**：靈活的元素定位策略和等待機制

- **挑戰**：確保測試的穩定性和可靠性
- **解決方案**：自定義重試機制和詳細的錯誤處理

- **挑戰**：模擬高併發場景
- **解決方案**：使用 Locust 的分佈式架構

---

# 未來改進方向

- 添加移動應用測試支持
- 整合 AI 輔助的測試用例生成
- 實現測試數據的智能管理
- 擴展安全測試功能
- 優化測試執行效率

---

# 總結

- 全面的自動化測試框架
- 展示了測試設計、編程和 DevOps 技能
- 可立即應用於實際項目

---

# 謝謝！

## 問題與討論
