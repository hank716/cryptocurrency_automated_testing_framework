import pytest
import os
import sys
import logging
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager

# Add project root to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.config_manager import ConfigManager

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


@pytest.fixture(scope="session")
def config() -> ConfigManager:
    """
    Fixture to provide configuration manager.
    
    Returns:
        ConfigManager instance
    """
    return ConfigManager()


@pytest.fixture(scope="function")
def chrome_driver(config: ConfigManager):
    """
    Fixture to provide Chrome WebDriver.
    
    Args:
        config: ConfigManager fixture
        
    Returns:
        WebDriver instance
    """
    web_config = config.get_web_config()
    
    # Configure Chrome options
    chrome_options = Options()
    if web_config.get('headless', True):
        chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--window-size=1920,1080')
    
    # Initialize Chrome WebDriver
    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=chrome_options
    )
    
    # Set implicit wait time
    driver.implicitly_wait(web_config.get('timeout', 10))
    
    yield driver
    
    # Cleanup
    driver.quit()


@pytest.fixture(scope="function")
def firefox_driver(config: ConfigManager):
    """
    Fixture to provide Firefox WebDriver.
    
    Args:
        config: ConfigManager fixture
        
    Returns:
        WebDriver instance
    """
    web_config = config.get_web_config()
    
    # Configure Firefox options
    firefox_options = webdriver.FirefoxOptions()
    if web_config.get('headless', True):
        firefox_options.add_argument('--headless')
    
    # Initialize Firefox WebDriver
    driver = webdriver.Firefox(
        service=Service(GeckoDriverManager().install()),
        options=firefox_options
    )
    
    # Set window size
    driver.set_window_size(1920, 1080)
    
    # Set implicit wait time
    driver.implicitly_wait(web_config.get('timeout', 10))
    
    yield driver
    
    # Cleanup
    driver.quit()


@pytest.fixture(params=["chrome", "firefox"])
def browser(request, chrome_driver, firefox_driver):
    """
    Fixture to provide WebDriver for cross-browser testing.
    
    Args:
        request: Pytest request object
        chrome_driver: Chrome WebDriver fixture
        firefox_driver: Firefox WebDriver fixture
        
    Returns:
        WebDriver instance
    """
    if request.param == "chrome":
        return chrome_driver
    elif request.param == "firefox":
        return firefox_driver


def pytest_addoption(parser):
    """
    Add custom command line options.
    
    Args:
        parser: Pytest argument parser
    """
    parser.addoption(
        "--browser",
        action="store",
        default="chrome",
        help="Browser to use for tests (chrome or firefox)"
    )
    parser.addoption(
        "--headless",
        action="store_true",
        default=True,
        help="Run browser in headless mode"
    )


def pytest_configure(config):
    """
    Configure pytest.
    
    Args:
        config: Pytest configuration
    """
    # Register custom markers
    config.addinivalue_line("markers", "web: mark a test as a web UI test")
    config.addinivalue_line("markers", "smoke: mark a test as a smoke test")
    config.addinivalue_line("markers", "regression: mark a test as a regression test")


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    Hook to capture screenshots on test failure.
    
    Args:
        item: Test item
        call: Test call
    """
    # Execute all other hooks to obtain the report object
    outcome = yield
    report = outcome.get_result()
    
    # Only capture screenshot if the test failed and it's a web test
    if report.when == "call" and report.failed and hasattr(item, "funcargs"):
        for driver_name in ["chrome_driver", "firefox_driver", "browser"]:
            if driver_name in item.funcargs:
                driver = item.funcargs[driver_name]
                try:
                    # Get the directory of the current file
                    current_dir = os.path.dirname(os.path.abspath(__file__))
                    # Go up one level to the project root
                    project_root = os.path.dirname(current_dir)
                    # Screenshot directory
                    screenshot_dir = os.path.join(project_root, 'reports', 'screenshots')
                    os.makedirs(screenshot_dir, exist_ok=True)
                    
                    # Take screenshot
                    screenshot_path = os.path.join(
                        screenshot_dir, 
                        f"{item.name}_{driver_name}_{call.when}.png"
                    )
                    driver.save_screenshot(screenshot_path)
                    logger.info(f"Screenshot saved to {screenshot_path}")
                except Exception as e:
                    logger.error(f"Failed to capture screenshot: {e}")
                break
