from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import logging

from .base_page import BasePage

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class HomePage(BasePage):
    """
    Home Page object for CoinMarketCap website.
    
    This class provides methods for interacting with elements on the
    CoinMarketCap home page.
    """
    
    # Locators
    SEARCH_INPUT = (By.CSS_SELECTOR, "input[placeholder='Search']")
    CRYPTOCURRENCIES_TAB = (By.XPATH, "//a[contains(text(), 'Cryptocurrencies')]")
    EXCHANGES_TAB = (By.XPATH, "//a[contains(text(), 'Exchanges')]")
    CRYPTO_TABLE = (By.CSS_SELECTOR, "table.cmc-table")
    CRYPTO_ROWS = (By.CSS_SELECTOR, "table.cmc-table tbody tr")
    CRYPTO_NAME_CELLS = (By.CSS_SELECTOR, "table.cmc-table tbody tr td:nth-child(3)")
    PAGINATION_NEXT = (By.CSS_SELECTOR, "button[aria-label='Next page']")
    COOKIE_BANNER_ACCEPT = (By.CSS_SELECTOR, "button.cookie-policy-banner-actions__button")
    
    def __init__(self, driver, base_url=None):
        """
        Initialize the HomePage with WebDriver instance.
        
        Args:
            driver: WebDriver instance
            base_url: Base URL for the website
        """
        super().__init__(driver, base_url)
    
    def open(self):
        """
        Open the home page.
        
        Returns:
            Self for method chaining
        """
        logger.info("Opening CoinMarketCap home page")
        self.navigate_to("")
        self.dismiss_cookie_banner()
        return self
    
    def dismiss_cookie_banner(self):
        """
        Dismiss the cookie banner if present.
        
        Returns:
            Self for method chaining
        """
        try:
            if self.is_element_present(self.COOKIE_BANNER_ACCEPT, timeout=5):
                self.click(self.COOKIE_BANNER_ACCEPT)
                logger.info("Cookie banner dismissed")
        except Exception as e:
            logger.warning(f"Failed to dismiss cookie banner: {e}")
        
        return self
    
    def search(self, query):
        """
        Search for a cryptocurrency.
        
        Args:
            query: Search query
            
        Returns:
            Self for method chaining
        """
        logger.info(f"Searching for: {query}")
        self.input_text(self.SEARCH_INPUT, query)
        self.find_element(self.SEARCH_INPUT).send_keys(Keys.ENTER)
        return self
    
    def go_to_cryptocurrencies(self):
        """
        Navigate to the Cryptocurrencies page.
        
        Returns:
            Self for method chaining
        """
        logger.info("Navigating to Cryptocurrencies page")
        self.click(self.CRYPTOCURRENCIES_TAB)
        return self
    
    def go_to_exchanges(self):
        """
        Navigate to the Exchanges page.
        
        Returns:
            Self for method chaining
        """
        logger.info("Navigating to Exchanges page")
        self.click(self.EXCHANGES_TAB)
        return self
    
    def get_crypto_table(self):
        """
        Get the cryptocurrency table.
        
        Returns:
            WebElement of the cryptocurrency table
        """
        return self.find_element(self.CRYPTO_TABLE)
    
    def get_crypto_rows(self):
        """
        Get all cryptocurrency rows.
        
        Returns:
            List of WebElements representing cryptocurrency rows
        """
        return self.find_elements(self.CRYPTO_ROWS)
    
    def get_crypto_names(self):
        """
        Get all cryptocurrency names from the table.
        
        Returns:
            List of cryptocurrency names
        """
        name_cells = self.find_elements(self.CRYPTO_NAME_CELLS)
        return [cell.text for cell in name_cells]
    
    def go_to_next_page(self):
        """
        Navigate to the next page of results.
        
        Returns:
            Self for method chaining
        """
        logger.info("Navigating to next page")
        self.click(self.PAGINATION_NEXT)
        return self
    
    def is_next_page_available(self):
        """
        Check if next page is available.
        
        Returns:
            True if next page is available, False otherwise
        """
        try:
            next_button = self.find_element(self.PAGINATION_NEXT, timeout=5)
            return next_button.is_enabled()
        except:
            return False
    
    def click_on_cryptocurrency(self, name):
        """
        Click on a cryptocurrency by name.
        
        Args:
            name: Name of the cryptocurrency
            
        Returns:
            Self for method chaining
        """
        logger.info(f"Clicking on cryptocurrency: {name}")
        locator = (By.XPATH, f"//td[contains(text(), '{name}')]")
        self.click(locator)
        return self
