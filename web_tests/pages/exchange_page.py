from selenium.webdriver.common.by import By
import logging

from .base_page import BasePage

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class ExchangePage(BasePage):
    """
    Exchange Page object for CoinMarketCap website.
    
    This class provides methods for interacting with elements on the
    exchange details page.
    """
    
    # Locators
    EXCHANGE_NAME = (By.CSS_SELECTOR, "h2.nameHeader")
    EXCHANGE_RANK = (By.CSS_SELECTOR, "div.namePillPrimary")
    EXCHANGE_SCORE = (By.XPATH, "//div[contains(text(), 'Exchange Score')]/following-sibling::div")
    VOLUME_24H = (By.XPATH, "//div[contains(text(), 'Volume')]/following-sibling::div")
    MARKETS = (By.XPATH, "//div[contains(text(), 'Markets')]/following-sibling::div")
    COINS = (By.XPATH, "//div[contains(text(), 'Coins')]/following-sibling::div")
    MARKETS_TAB = (By.XPATH, "//button[contains(text(), 'Markets')]")
    INFO_TAB = (By.XPATH, "//button[contains(text(), 'Info')]")
    MARKET_PAIRS_TABLE = (By.CSS_SELECTOR, "table.cmc-table")
    MARKET_PAIRS_ROWS = (By.CSS_SELECTOR, "table.cmc-table tbody tr")
    
    def __init__(self, driver, base_url=None):
        """
        Initialize the ExchangePage with WebDriver instance.
        
        Args:
            driver: WebDriver instance
            base_url: Base URL for the website
        """
        super().__init__(driver, base_url)
    
    def open_exchange_page(self, exchange_id):
        """
        Open a specific exchange page by ID.
        
        Args:
            exchange_id: Exchange ID
            
        Returns:
            Self for method chaining
        """
        logger.info(f"Opening exchange page for ID: {exchange_id}")
        self.navigate_to(f"exchanges/{exchange_id}")
        return self
    
    def get_exchange_name(self):
        """
        Get the exchange name.
        
        Returns:
            Exchange name
        """
        return self.get_text(self.EXCHANGE_NAME)
    
    def get_exchange_rank(self):
        """
        Get the exchange rank.
        
        Returns:
            Exchange rank as a string
        """
        rank_text = self.get_text(self.EXCHANGE_RANK)
        # Extract rank number from text like "Rank #1"
        return rank_text.replace("Rank #", "")
    
    def get_exchange_score(self):
        """
        Get the exchange score.
        
        Returns:
            Exchange score as a string
        """
        return self.get_text(self.EXCHANGE_SCORE)
    
    def get_volume_24h(self):
        """
        Get the 24-hour trading volume.
        
        Returns:
            24-hour trading volume as a string
        """
        return self.get_text(self.VOLUME_24H)
    
    def get_markets_count(self):
        """
        Get the number of markets.
        
        Returns:
            Number of markets as a string
        """
        return self.get_text(self.MARKETS)
    
    def get_coins_count(self):
        """
        Get the number of coins.
        
        Returns:
            Number of coins as a string
        """
        return self.get_text(self.COINS)
    
    def go_to_markets_tab(self):
        """
        Navigate to the Markets tab.
        
        Returns:
            Self for method chaining
        """
        logger.info("Navigating to Markets tab")
        self.click(self.MARKETS_TAB)
        return self
    
    def go_to_info_tab(self):
        """
        Navigate to the Info tab.
        
        Returns:
            Self for method chaining
        """
        logger.info("Navigating to Info tab")
        self.click(self.INFO_TAB)
        return self
    
    def get_market_pairs_table(self):
        """
        Get the market pairs table.
        
        Returns:
            WebElement of the market pairs table
        """
        return self.find_element(self.MARKET_PAIRS_TABLE)
    
    def get_market_pairs_rows(self):
        """
        Get all market pairs rows.
        
        Returns:
            List of WebElements representing market pairs rows
        """
        return self.find_elements(self.MARKET_PAIRS_ROWS)
    
    def get_market_pairs_count(self):
        """
        Get the number of market pairs.
        
        Returns:
            Number of market pairs
        """
        rows = self.get_market_pairs_rows()
        return len(rows)
    
    def get_exchange_data(self):
        """
        Get all exchange data.
        
        Returns:
            Dictionary containing exchange data
        """
        data = {
            "name": self.get_exchange_name(),
            "rank": self.get_exchange_rank(),
            "score": self.get_exchange_score(),
            "volume_24h": self.get_volume_24h(),
            "markets_count": self.get_markets_count(),
            "coins_count": self.get_coins_count()
        }
        
        logger.info(f"Exchange data: {data}")
        return data
