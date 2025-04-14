import pytest
import os
import sys
import logging
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.config_manager import ConfigManager

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

@pytest.fixture(scope="session")
def config() -> ConfigManager:
    return ConfigManager()

@pytest.fixture(scope="function")
def chrome_driver(config: ConfigManager):
    web_config = config.get_web_config()
    options = Options()
    if web_config.get('headless', True):
        # 使用新版 headless 模式並加上 disable-gpu 避免 GPU 問題
        options.add_argument('--headless=new')
        options.add_argument('--disable-gpu')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--window-size=1920,1080')
    # 取得 chromedriver 的安裝路徑
    driver_path = ChromeDriverManager().install()
    # 如果返回的路徑包含 "THIRD_PARTY_NOTICES"，則去掉這段字串以取得正確的執行檔
    if "THIRD_PARTY_NOTICES" in driver_path:
        driver_path = driver_path.replace("THIRD_PARTY_NOTICES.", "")
    logger.info(f"Using chromedriver path: {driver_path}")
    driver = webdriver.Chrome(service=Service(driver_path), options=options)
    driver.implicitly_wait(web_config.get('timeout', 10))
    yield driver
    driver.quit()

@pytest.fixture(scope="function")
def firefox_driver(config: ConfigManager):
    web_config = config.get_web_config()
    firefox_options = webdriver.FirefoxOptions()
    if web_config.get('headless', True):
        firefox_options.add_argument('--headless')
    driver = webdriver.Firefox(service=Service(GeckoDriverManager().install()), options=firefox_options)
    driver.set_window_size(1920, 1080)
    driver.implicitly_wait(web_config.get('timeout', 10))
    yield driver
    driver.quit()

@pytest.fixture(params=["chrome", "firefox"])
def browser(request, chrome_driver, firefox_driver):
    if request.param == "chrome":
        return chrome_driver
    elif request.param == "firefox":
        return firefox_driver

def pytest_addoption(parser):
    parser.addoption("--browser", action="store", default="chrome", help="Browser to use for tests (chrome or firefox)")
    parser.addoption("--headless", action="store_true", default=True, help="Run browser in headless mode")

def pytest_configure(config):
    config.addinivalue_line("markers", "web: mark a test as a web UI test")
    config.addinivalue_line("markers", "smoke: mark a test as a smoke test")
    config.addinivalue_line("markers", "regression: mark a test as a regression test")

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    # 於 call 階段（無論通過或失敗）進行截圖
    if report.when == "call" and hasattr(item, "funcargs"):
        for driver_name in ["chrome_driver", "firefox_driver", "browser"]:
            if driver_name in item.funcargs:
                driver = item.funcargs[driver_name]
                try:
                    timestamp = os.getenv("TEST_TIMESTAMP", "default")
                    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
                    screenshot_dir = os.path.join(project_root, "reports", timestamp, "screenshots")
                    os.makedirs(screenshot_dir, exist_ok=True)
                    # 檔名中不論測試通過與否，都輸出截圖
                    screenshot_path = os.path.join(screenshot_dir, f"{item.name}_{driver_name}.png")
                    driver.save_screenshot(screenshot_path)
                    logger.info(f"Screenshot saved to {screenshot_path}")
                except Exception as e:
                    logger.error(f"Screenshot capture failed: {e}")
                break
