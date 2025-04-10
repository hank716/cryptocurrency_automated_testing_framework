from selenium.webdriver.common.by import By
import logging

from .base_page import BasePage

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class CoinPage(BasePage):
    """
    Coin Page object for CoinMarketCap website.
    
    This class provides methods for interacting with elements on the
    cryptocurrency details page.
    """
    
    # Locators
    COIN_NAME = (By.CSS_SELECTOR, "h2.nameHeader")
    COIN_SYMBOL = (By.CSS_SELECTOR, "span.nameSymbol")
    COIN_PRICE = (By.CSS_SELECTOR, "div.priceValue")
    MARKET_CAP = (By.XPATH, "//div[contains(text(), 'Market Cap')]/following-sibling::div")
    VOLUME_24H = (By.XPATH, "//div[contains(text(), 'Volume')]/following-sibling::div")
    CIRCULATING_SUPPLY = (By.XPATH, "//div[contains(text(), 'Circulating Supply')]/following-sibling::div")
    PRICE_CHART = (By.CSS_SELECTOR, "div.chart")
    PRICE_CHANGE_24H = (By.CSS_SELECTOR, "span.sc-15yy2pl-0")
    MARKETS_TAB = (By.XPATH, "//button[contains(text(), 'Markets')]")
    HISTORICAL_DATA_TAB = (By.XPATH, "//button[contains(text(), 'Historical Data')]")
    
    def __init__(self, driver, base_url=None):
        """
        Initialize the CoinPage with WebDriver instance.
        
        Args:
            driver: WebDriver instance
            base_url: Base URL for the website
        """
        super().__init__(driver, base_url)
    
    def open_coin_page(self, coin_id):
        """
        Open a specific cryptocurrency page by ID.
        
        Args:
            coin_id: Cryptocurrency ID
            
        Returns:
            Self for method chaining
        """
        logger.info(f"Opening cryptocurrency page for ID: {coin_id}")
        self.navigate_to(f"currencies/{coin_id}")
        return self
    
    def get_coin_name(self):
        """
        Get the cryptocurrency name.
        
        Returns:
            Cryptocurrency name
        """
        return self.get_text(self.COIN_NAME)
    
    def get_coin_symbol(self):
        """
        Get the cryptocurrency symbol.
        
        Returns:
            Cryptocurrency symbol
        """
        return self.get_text(self.COIN_SYMBOL)
    
    def get_coin_price(self):
        """
        Get the cryptocurrency price.
        
        Returns:
            Cryptocurrency price as a string
        """
        price_text = self.get_text(self.COIN_PRICE)
        return price_text
    
    def get_market_cap(self):
        """
        Get the market capitalization.
        
        Returns:
            Market capitalization as a string
        """
        return self.get_text(self.MARKET_CAP)
    
    def get_volume_24h(self):
        """
        Get the 24-hour trading volume.
        
        Returns:
            24-hour trading volume as a string
        """
        return self.get_text(self.VOLUME_24H)
    
    def get_circulating_supply(self):
        """
        Get the circulating supply.
        
        Returns:
            Circulating supply as a string
        """
        return self.get_text(self.CIRCULATING_SUPPLY)
    
    def get_price_change_24h(self):
        """
        Get the 24-hour price change percentage.
        
        Returns:
            24-hour price change percentage as a string
        """
        return self.get_text(self.PRICE_CHANGE_24H)
    
    def is_price_chart_displayed(self):
        """
        Check if the price chart is displayed.
        
        Returns:
            True if the price chart is displayed, False otherwise
        """
        return self.is_element_present(self.PRICE_CHART)
    
    def go_to_markets_tab(self):
        """
        Navigate to the Markets tab.
        
        Returns:
            Self for method chaining
        """
        logger.info("Navigating to Markets tab")
        self.click(self.MARKETS_TAB)
        return self
    
    def go_to_historical_data_tab(self):
        """
        Navigate to the Historical Data tab.
        
        Returns:
            Self for method chaining
        """
        logger.info("Navigating to Historical Data tab")
        self.click(self.HISTORICAL_DATA_TAB)
        return self
    
    def get_coin_data(self):
        """
        Get all cryptocurrency data.
        
        Returns:
            Dictionary containing cryptocurrency data
        """
        data = {
            "name": self.get_coin_name(),
            "symbol": self.get_coin_symbol(),
            "price": self.get_coin_price(),
            "market_cap": self.get_market_cap(),
            "volume_24h": self.get_volume_24h(),
            "circulating_supply": self.get_circulating_supply(),
            "price_change_24h": self.get_price_change_24h()
        }
        
        logger.info(f"Coin data: {data}")
        return data
