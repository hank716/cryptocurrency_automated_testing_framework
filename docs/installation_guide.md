# 安裝與使用指南

## 環境需求

- Python 3.10 或更高版本
- Chrome 瀏覽器（用於 Web UI 測試）
- Git（用於版本控制和 CI/CD 整合）
- 網絡連接（用於 API 測試和依賴安裝）

## 安裝步驟

### 1. 克隆專案

```bash
git clone https://github.com/yourusername/crypto_qa_framework.git
cd crypto_qa_framework
```

### 2. 創建虛擬環境（推薦）

```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# 或
venv\Scripts\activate  # Windows
```

### 3. 安裝依賴

```bash
pip install -r requirements.txt
```

## 配置設定

框架使用 YAML 格式的配置文件，位於 `config/default.yaml`。您可以根據需要修改以下配置：

### API 測試配置

```yaml
api:
  base_url: https://sandbox-api.coinmarketcap.com
  timeout: 30
  retry_count: 3
  api_key: your_api_key_here  # 請替換為您的 API 密鑰
```

### Web 測試配置

```yaml
web:
  base_url: https://coinmarketcap.com
  timeout: 10
  headless: true  # 無頭模式，設為 false 可查看瀏覽器操作
  screenshot_dir: reports/screenshots
```

### 性能測試配置

```yaml
performance:
  host: https://sandbox-api.coinmarketcap.com
  users: 10  # 模擬用戶數
  spawn_rate: 1  # 每秒新增用戶數
  run_time: 1m  # 運行時間
```

## 使用方法

### 運行所有測試

使用提供的 Shell 腳本可以一鍵運行所有測試：

```bash
./run_tests.sh
```

### 運行特定測試模組

#### API 測試

```bash
pytest api_tests/ -v
```

#### Web UI 測試

```bash
pytest web_tests/test_cases/ -v
```

#### 性能測試

```bash
python performance_tests/test_scenarios/run_performance_tests.py --scenario normal
```

### 生成測試報告

添加 `--html` 參數可以生成 HTML 格式的測試報告：

```bash
pytest api_tests/ -v --html=reports/api_test_report.html
```

### 使用 GitHub Actions

如果您已將專案推送到 GitHub，可以通過以下方式觸發 CI/CD 流程：

1. 推送代碼到 `main` 或 `develop` 分支
2. 創建 Pull Request
3. 在 GitHub Actions 頁面手動觸發工作流

## 測試報告查看

測試完成後，報告將生成在 `reports` 目錄下：

- API 測試報告：`reports/api_reports/`
- Web 測試報告：`reports/web_reports/`
- 性能測試報告：`reports/performance_reports/`
- 合併報告：`reports/combined_reports/`

## 常見問題排解

### Q: 安裝依賴時出現錯誤

確保您使用的是 Python 3.10 或更高版本，並嘗試使用以下命令更新 pip：

```bash
python -m pip install --upgrade pip
```

### Q: Web 測試無法啟動瀏覽器

確保已安裝 Chrome 瀏覽器，並檢查 WebDriver 是否正確安裝：

```bash
pip install webdriver-manager --upgrade
```

### Q: 性能測試報告不顯示圖表

確保已安裝所有依賴，特別是 Locust 相關的包：

```bash
pip install locust
```

### Q: CI/CD 工作流失敗

檢查 GitHub Actions 日誌以獲取詳細錯誤信息，常見原因包括：
- 缺少環境變量或密鑰
- 測試失敗
- 依賴安裝問題

## 擴展框架

### 添加新的 API 測試

1. 在 `api_tests/` 目錄下創建新的測試文件
2. 使用 `pytest` 裝飾器和斷言編寫測試案例
3. 利用 `utils/api_client.py` 進行 API 調用

### 添加新的 Web UI 測試

1. 如需要，在 `web_tests/pages/` 目錄下創建新的頁面對象
2. 在 `web_tests/test_cases/` 目錄下創建新的測試文件
3. 使用頁面對象模式編寫測試案例

### 添加新的性能測試

1. 在 `performance_tests/locustfiles/` 目錄下創建新的 Locust 文件
2. 定義用戶行為和任務
3. 在 `run_performance_tests.py` 中添加新的測試場景
