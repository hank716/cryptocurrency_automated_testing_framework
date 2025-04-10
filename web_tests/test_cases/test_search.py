import pytest
import logging
from selenium.webdriver.remote.webdriver import WebDriver

from web_tests.pages.home_page import HomePage

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


@pytest.mark.web
class TestSearch:
    """
    Test suite for search functionality.
    
    This class contains tests for searching cryptocurrencies
    on the CoinMarketCap website.
    """
    
    def test_search_valid_cryptocurrency(self, chrome_driver: WebDriver):
        """
        Test searching for a valid cryptocurrency.
        
        Args:
            chrome_driver: Chrome WebDriver fixture
        """
        # Initialize home page
        home_page = HomePage(chrome_driver)
        
        # Open home page
        home_page.open()
        
        # Search for Bitcoin
        home_page.search("Bitcoin")
        
        # Verify search results
        crypto_names = home_page.get_crypto_names()
        assert any("Bitcoin" in name for name in crypto_names)
        
        logger.info("Search for valid cryptocurrency successful")
    
    def test_search_by_symbol(self, chrome_driver: WebDriver):
        """
        Test searching for a cryptocurrency by symbol.
        
        Args:
            chrome_driver: Chrome WebDriver fixture
        """
        # Initialize home page
        home_page = HomePage(chrome_driver)
        
        # Open home page
        home_page.open()
        
        # Search for Ethereum by symbol
        home_page.search("ETH")
        
        # Verify search results
        crypto_names = home_page.get_crypto_names()
        assert any("Ethereum" in name for name in crypto_names)
        
        logger.info("Search by symbol successful")
    
    def test_search_partial_name(self, chrome_driver: WebDriver):
        """
        Test searching with a partial cryptocurrency name.
        
        Args:
            chrome_driver: Chrome WebDriver fixture
        """
        # Initialize home page
        home_page = HomePage(chrome_driver)
        
        # Open home page
        home_page.open()
        
        # Search for partial name
        home_page.search("Carda")  # Should find Cardano
        
        # Verify search results
        crypto_names = home_page.get_crypto_names()
        assert any("Cardano" in name for name in crypto_names)
        
        logger.info("Search with partial name successful")
    
    def test_search_invalid_cryptocurrency(self, chrome_driver: WebDriver):
        """
        Test searching for an invalid cryptocurrency.
        
        Args:
            chrome_driver: Chrome WebDriver fixture
        """
        # Initialize home page
        home_page = HomePage(chrome_driver)
        
        # Open home page
        home_page.open()
        
        # Search for invalid cryptocurrency
        home_page.search("InvalidCryptoXYZ123")
        
        # Verify no results or "No results found" message
        crypto_rows = home_page.get_crypto_rows()
        assert len(crypto_rows) == 0 or "No results found" in chrome_driver.page_source
        
        logger.info("Search for invalid cryptocurrency handled correctly")
    
    def test_search_case_insensitivity(self, chrome_driver: WebDriver):
        """
        Test that search is case-insensitive.
        
        Args:
            chrome_driver: Chrome WebDriver fixture
        """
        # Initialize home page
        home_page = HomePage(chrome_driver)
        
        # Open home page
        home_page.open()
        
        # Search with lowercase
        home_page.search("bitcoin")
        
        # Verify search results
        crypto_names = home_page.get_crypto_names()
        assert any("Bitcoin" in name for name in crypto_names)
        
        # Open home page again
        home_page.open()
        
        # Search with mixed case
        home_page.search("BiTcOiN")
        
        # Verify search results
        crypto_names = home_page.get_crypto_names()
        assert any("Bitcoin" in name for name in crypto_names)
        
        logger.info("Case-insensitive search test successful")
    
    @pytest.mark.parametrize("search_term, expected_result", [
        ("Bitcoin", "Bitcoin"),
        ("ETH", "Ethereum"),
        ("XRP", "XRP"),
        ("ADA", "Cardano"),
        ("SOL", "Solana")
    ])
    def test_multiple_search_terms(self, chrome_driver: WebDriver, search_term, expected_result):
        """
        Test searching for multiple cryptocurrencies.
        
        Args:
            chrome_driver: Chrome WebDriver fixture
            search_term: Term to search for
            expected_result: Expected cryptocurrency name in results
        """
        # Initialize home page
        home_page = HomePage(chrome_driver)
        
        # Open home page
        home_page.open()
        
        # Search for the term
        home_page.search(search_term)
        
        # Verify search results
        crypto_names = home_page.get_crypto_names()
        assert any(expected_result in name for name in crypto_names)
        
        logger.info(f"Search for '{search_term}' found '{expected_result}' successfully")
