import pytest
import os
import sys
import logging
from typing import Dict, Any

# Add project root to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.config_manager import ConfigManager
from utils.api_client import ApiClient

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


@pytest.fixture(scope="session")
def api_client(config: ConfigManager) -> ApiClient:
    """
    Fixture to provide API client.
    
    Args:
        config: ConfigManager fixture
        
    Returns:
        ApiClient instance
    """
    api_config = config.get_api_config()
    
    client = ApiClient(
        base_url=api_config.get('base_url'),
        api_key=api_config.get('api_key'),
        timeout=api_config.get('timeout', 30),
        retry_count=api_config.get('retry_count', 3)
    )
    
    yield client
    
    # Cleanup
    client.close()


@pytest.fixture
def cryptocurrency_data() -> Dict[str, Any]:
    """
    Fixture to provide cryptocurrency test data.
    
    Returns:
        Dictionary containing cryptocurrency test data
    """
    return {
        "id": 1,
        "name": "Bitcoin",
        "symbol": "BTC",
        "price_usd": 45000.0,
        "market_cap_usd": 850000000000,
        "volume_24h_usd": 25000000000,
        "percent_change_24h": 2.5,
        "last_updated": "2023-01-01T00:00:00Z"
    }


@pytest.fixture
def exchange_data() -> Dict[str, Any]:
    """
    Fixture to provide exchange test data.
    
    Returns:
        Dictionary containing exchange test data
    """
    return {
        "id": 1,
        "name": "Binance",
        "volume_24h_usd": 15000000000,
        "markets_count": 1200,
        "coins_count": 350,
        "last_updated": "2023-01-01T00:00:00Z"
    }


def pytest_configure(config):
    """
    Configure pytest.
    
    Args:
        config: Pytest configuration
    """
    # Register custom markers
    config.addinivalue_line("markers", "api: mark a test as an API test")
    config.addinivalue_line("markers", "slow: mark a test as slow")
    config.addinivalue_line("markers", "performance: mark a test as a performance test")


def pytest_addoption(parser):
    """
    Add custom command line options.
    
    Args:
        parser: Pytest argument parser
    """
    parser.addoption(
        "--api-url",
        action="store",
        default=None,
        help="Base URL for API tests"
    )
    parser.addoption(
        "--api-key",
        action="store",
        default=None,
        help="API key for authentication"
    )


def pytest_collection_modifyitems(config, items):
    """
    Modify test items based on command line options.
    
    Args:
        config: Pytest configuration
        items: Test items
    """
    # Skip slow tests if --skip-slow is specified
    if config.getoption("--skip-slow", default=False):
        skip_slow = pytest.mark.skip(reason="--skip-slow option provided")
        for item in items:
            if "slow" in item.keywords:
                item.add_marker(skip_slow)
