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
class TestNavigation:
    """
    Test suite for website navigation.
    
    This class contains tests for navigating between different pages
    of the CoinMarketCap website.
    """
    
    def test_home_page_load(self, chrome_driver: WebDriver):
        """
        Test that the home page loads correctly.
        
        Args:
            chrome_driver: Chrome WebDriver fixture
        """
        # Initialize home page
        home_page = HomePage(chrome_driver)
        
        # Open home page
        home_page.open()
        
        # Verify page title
        title = home_page.get_title()
        assert "CoinMarketCap" in title
        
        # Verify cryptocurrency table is displayed
        assert home_page.is_element_present(home_page.CRYPTO_TABLE)
        
        # Verify there are cryptocurrency rows
        crypto_rows = home_page.get_crypto_rows()
        assert len(crypto_rows) > 0
        
        logger.info(f"Home page loaded successfully with {len(crypto_rows)} cryptocurrency rows")
    
    def test_navigation_to_cryptocurrencies(self, chrome_driver: WebDriver):
        """
        Test navigation to the Cryptocurrencies page.
        
        Args:
            chrome_driver: Chrome WebDriver fixture
        """
        # Initialize home page
        home_page = HomePage(chrome_driver)
        
        # Open home page
        home_page.open()
        
        # Navigate to Cryptocurrencies page
        home_page.go_to_cryptocurrencies()
        
        # Verify URL contains "cryptocurrencies"
        current_url = home_page.get_current_url()
        assert "cryptocurrencies" in current_url
        
        # Verify cryptocurrency table is displayed
        assert home_page.is_element_present(home_page.CRYPTO_TABLE)
        
        logger.info("Navigation to Cryptocurrencies page successful")
    
    def test_navigation_to_exchanges(self, chrome_driver: WebDriver):
        """
        Test navigation to the Exchanges page.
        
        Args:
            chrome_driver: Chrome WebDriver fixture
        """
        # Initialize home page
        home_page = HomePage(chrome_driver)
        
        # Open home page
        home_page.open()
        
        # Navigate to Exchanges page
        home_page.go_to_exchanges()
        
        # Verify URL contains "exchanges"
        current_url = home_page.get_current_url()
        assert "exchanges" in current_url
        
        logger.info("Navigation to Exchanges page successful")
    
    def test_pagination(self, chrome_driver: WebDriver):
        """
        Test pagination on the Cryptocurrencies page.
        
        Args:
            chrome_driver: Chrome WebDriver fixture
        """
        # Initialize home page
        home_page = HomePage(chrome_driver)
        
        # Open home page
        home_page.open()
        
        # Get cryptocurrencies on first page
        first_page_cryptos = home_page.get_crypto_names()
        
        # Navigate to next page
        if home_page.is_next_page_available():
            home_page.go_to_next_page()
            
            # Get cryptocurrencies on second page
            second_page_cryptos = home_page.get_crypto_names()
            
            # Verify different cryptocurrencies are displayed
            assert first_page_cryptos != second_page_cryptos
            
            logger.info("Pagination test successful")
        else:
            logger.warning("Next page not available, skipping pagination test")
            pytest.skip("Next page not available")
    
    def test_navigation_to_coin_page(self, chrome_driver: WebDriver):
        """
        Test navigation to a specific cryptocurrency page.
        
        Args:
            chrome_driver: Chrome WebDriver fixture
        """
        # Initialize home page
        home_page = HomePage(chrome_driver)
        
        # Open home page
        home_page.open()
        
        # Get the first cryptocurrency name
        crypto_names = home_page.get_crypto_names()
        if not crypto_names:
            pytest.skip("No cryptocurrencies found")
        
        # Navigate to Bitcoin page directly
        coin_page = CoinPage(chrome_driver)
        coin_page.open_coin_page("bitcoin")
        
        # Verify coin name is displayed
        assert coin_page.is_element_present(coin_page.COIN_NAME)
        
        # Verify price is displayed
        assert coin_page.is_element_present(coin_page.COIN_PRICE)
        
        # Verify price chart is displayed
        assert coin_page.is_price_chart_displayed()
        
        logger.info("Navigation to coin page successful")
    
    def test_browser_navigation(self, chrome_driver: WebDriver):
        """
        Test browser navigation (back and forward).
        
        Args:
            chrome_driver: Chrome WebDriver fixture
        """
        # Initialize pages
        home_page = HomePage(chrome_driver)
        coin_page = CoinPage(chrome_driver)
        
        # Open home page
        home_page.open()
        home_url = home_page.get_current_url()
        
        # Navigate to Bitcoin page
        coin_page.open_coin_page("bitcoin")
        coin_url = coin_page.get_current_url()
        
        # Verify URLs are different
        assert home_url != coin_url
        
        # Navigate back
        coin_page.go_back()
        
        # Verify we're back on the home page
        current_url = home_page.get_current_url()
        assert current_url == home_url
        
        # Navigate forward
        home_page.go_forward()
        
        # Verify we're back on the coin page
        current_url = coin_page.get_current_url()
        assert current_url == coin_url
        
        logger.info("Browser navigation test successful")
