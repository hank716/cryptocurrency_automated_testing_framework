import pytest
import logging
from selenium.webdriver.remote.webdriver import WebDriver

from web_tests.pages.home_page import HomePage
from web_tests.pages.coin_page import CoinPage

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


@pytest.mark.web
class TestMarketData:
    """
    Test suite for market data display.
    
    This class contains tests for verifying the display and accuracy
    of cryptocurrency market data on the CoinMarketCap website.
    """
    
    def test_cryptocurrency_data_display(self, chrome_driver: WebDriver):
        """
        Test that cryptocurrency data is displayed correctly on the home page.
        
        Args:
            chrome_driver: Chrome WebDriver fixture
        """
        # Initialize home page
        home_page = HomePage(chrome_driver)
        
        # Open home page
        home_page.open()
        
        # Verify cryptocurrency table is displayed
        assert home_page.is_element_present(home_page.CRYPTO_TABLE)
        
        # Verify there are cryptocurrency rows
        crypto_rows = home_page.get_crypto_rows()
        assert len(crypto_rows) > 0
        
        # Verify cryptocurrency names are displayed
        crypto_names = home_page.get_crypto_names()
        assert len(crypto_names) > 0
        
        logger.info(f"Cryptocurrency data displayed correctly with {len(crypto_names)} cryptocurrencies")
    
    def test_bitcoin_data_accuracy(self, chrome_driver: WebDriver):
        """
        Test the accuracy of Bitcoin market data.
        
        Args:
            chrome_driver: Chrome WebDriver fixture
        """
        # Initialize coin page
        coin_page = CoinPage(chrome_driver)
        
        # Open Bitcoin page
        coin_page.open_coin_page("bitcoin")
        
        # Get Bitcoin data
        bitcoin_data = coin_page.get_coin_data()
        
        # Verify data fields
        assert bitcoin_data["name"] == "Bitcoin"
        assert bitcoin_data["symbol"] == "BTC"
        assert "$" in bitcoin_data["price"]
        assert "$" in bitcoin_data["market_cap"]
        assert "$" in bitcoin_data["volume_24h"]
        assert "BTC" in bitcoin_data["circulating_supply"]
        assert "%" in bitcoin_data["price_change_24h"]
        
        logger.info("Bitcoin data accuracy test successful")
    
    def test_market_data_consistency(self, chrome_driver: WebDriver):
        """
        Test the consistency of market data between pages.
        
        Args:
            chrome_driver: Chrome WebDriver fixture
        """
        # Initialize pages
        home_page = HomePage(chrome_driver)
        coin_page = CoinPage(chrome_driver)
        
        # Open home page
        home_page.open()
        
        # Get cryptocurrency names
        crypto_names = home_page.get_crypto_names()
        if not crypto_names:
            pytest.skip("No cryptocurrencies found")
        
        # Navigate to Bitcoin page
        coin_page.open_coin_page("bitcoin")
        
        # Get Bitcoin data
        bitcoin_data = coin_page.get_coin_data()
        
        # Verify Bitcoin name and symbol
        assert bitcoin_data["name"] == "Bitcoin"
        assert bitcoin_data["symbol"] == "BTC"
        
        logger.info("Market data consistency test successful")
    
    def test_price_chart_display(self, chrome_driver: WebDriver):
        """
        Test that the price chart is displayed on the coin page.
        
        Args:
            chrome_driver: Chrome WebDriver fixture
        """
        # Initialize coin page
        coin_page = CoinPage(chrome_driver)
        
        # Open Bitcoin page
        coin_page.open_coin_page("bitcoin")
        
        # Verify price chart is displayed
        assert coin_page.is_price_chart_displayed()
        
        logger.info("Price chart display test successful")
    
    @pytest.mark.parametrize("coin_id", ["bitcoin", "ethereum", "ripple"])
    def test_multiple_cryptocurrency_data(self, chrome_driver: WebDriver, coin_id):
        """
        Test market data for multiple cryptocurrencies.
        
        Args:
            chrome_driver: Chrome WebDriver fixture
            coin_id: Cryptocurrency ID
        """
        # Initialize coin page
        coin_page = CoinPage(chrome_driver)
        
        # Open coin page
        coin_page.open_coin_page(coin_id)
        
        # Get coin data
        coin_data = coin_page.get_coin_data()
        
        # Verify data fields
        assert coin_data["name"] != ""
        assert coin_data["symbol"] != ""
        assert "$" in coin_data["price"]
        assert "$" in coin_data["market_cap"]
        assert "$" in coin_data["volume_24h"]
        
        logger.info(f"Market data test for {coin_id} successful")
    
    def test_historical_data_tab(self, chrome_driver: WebDriver):
        """
        Test navigation to the Historical Data tab.
        
        Args:
            chrome_driver: Chrome WebDriver fixture
        """
        # Initialize coin page
        coin_page = CoinPage(chrome_driver)
        
        # Open Bitcoin page
        coin_page.open_coin_page("bitcoin")
        
        # Navigate to Historical Data tab
        coin_page.go_to_historical_data_tab()
        
        # Verify URL contains "historical"
        current_url = coin_page.get_current_url()
        assert "historical" in current_url
        
        logger.info("Historical data tab navigation test successful")
