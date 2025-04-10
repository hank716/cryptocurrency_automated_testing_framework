from locust import HttpUser, task, between
import logging
import random
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class CoinMarketCapUser(HttpUser):
    """
    Locust user class for testing CoinMarketCap website.
    
    This class simulates user behavior for web load testing,
    focusing on common user interactions with the website.
    """
    
    # Wait time between tasks (3-10 seconds)
    wait_time = between(3, 10)
    
    def on_start(self):
        """
        Initialize user session with a headless browser.
        """
        # Configure Chrome options
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--window-size=1920,1080')
        
        # Initialize Chrome WebDriver
        self.driver = webdriver.Chrome(options=chrome_options)
        self.driver.implicitly_wait(10)
        
        logger.info("Web user session started with headless browser")
    
    def on_stop(self):
        """
        Clean up resources when the test stops.
        """
        if hasattr(self, 'driver'):
            self.driver.quit()
        logger.info("Web user session ended")
    
    @task(3)
    def browse_home_page(self):
        """
        Task to browse the home page.
        
        This is a high-frequency task (weight: 3).
        """
        try:
            # Navigate to home page
            self.driver.get("https://coinmarketcap.com/")
            
            # Wait for cryptocurrency table to load
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "table.cmc-table"))
            )
            
            # Dismiss cookie banner if present
            try:
                cookie_button = self.driver.find_element(By.CSS_SELECTOR, "button.cookie-policy-banner-actions__button")
                cookie_button.click()
            except:
                pass
            
            # Scroll down to load more content
            self.driver.execute_script("window.scrollBy(0, 500);")
            
            # Log success
            logger.debug("Successfully browsed home page")
        except Exception as e:
            logger.error(f"Error browsing home page: {e}")
    
    @task(2)
    def search_cryptocurrency(self):
        """
        Task to search for a cryptocurrency.
        
        This is a medium-frequency task (weight: 2).
        """
        try:
            # Navigate to home page
            self.driver.get("https://coinmarketcap.com/")
            
            # Wait for page to load
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "table.cmc-table"))
            )
            
            # Common cryptocurrency names
            cryptos = ["Bitcoin", "Ethereum", "Ripple", "Cardano", "Solana", "Polkadot", "Dogecoin"]
            
            # Select a random cryptocurrency
            crypto = random.choice(cryptos)
            
            # Find search input
            search_input = self.driver.find_element(By.CSS_SELECTOR, "input[placeholder='Search']")
            search_input.clear()
            search_input.send_keys(crypto)
            
            # Wait for search results
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "table.cmc-table"))
            )
            
            # Log success
            logger.debug(f"Successfully searched for {crypto}")
        except Exception as e:
            logger.error(f"Error searching cryptocurrency: {e}")
    
    @task(1)
    def view_cryptocurrency_details(self):
        """
        Task to view cryptocurrency details.
        
        This is a low-frequency task (weight: 1).
        """
        try:
            # Common cryptocurrency IDs
            crypto_ids = ["bitcoin", "ethereum", "ripple", "cardano", "solana"]
            
            # Select a random cryptocurrency
            crypto_id = random.choice(crypto_ids)
            
            # Navigate to cryptocurrency page
            self.driver.get(f"https://coinmarketcap.com/currencies/{crypto_id}/")
            
            # Wait for price to load
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "div.priceValue"))
            )
            
            # Scroll down to view more content
            self.driver.execute_script("window.scrollBy(0, 700);")
            
            # Wait a bit to simulate reading
            import time
            time.sleep(random.uniform(1, 3))
            
            # Scroll down more
            self.driver.execute_script("window.scrollBy(0, 700);")
            
            # Log success
            logger.debug(f"Successfully viewed {crypto_id} details")
        except Exception as e:
            logger.error(f"Error viewing cryptocurrency details: {e}")
    
    @task(1)
    def browse_exchanges(self):
        """
        Task to browse exchanges.
        
        This is a low-frequency task (weight: 1).
        """
        try:
            # Navigate to exchanges page
            self.driver.get("https://coinmarketcap.com/exchanges/")
            
            # Wait for exchanges table to load
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "table.cmc-table"))
            )
            
            # Scroll down to load more content
            self.driver.execute_script("window.scrollBy(0, 500);")
            
            # Log success
            logger.debug("Successfully browsed exchanges page")
        except Exception as e:
            logger.error(f"Error browsing exchanges: {e}")
    
    @task(1)
    def navigate_between_pages(self):
        """
        Task to navigate between different pages.
        
        This is a low-frequency task (weight: 1).
        """
        try:
            # Navigate to home page
            self.driver.get("https://coinmarketcap.com/")
            
            # Wait for page to load
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "table.cmc-table"))
            )
            
            # Navigate to cryptocurrencies page
            self.driver.get("https://coinmarketcap.com/cryptocurrencies/")
            
            # Wait for page to load
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "table.cmc-table"))
            )
            
            # Navigate to exchanges page
            self.driver.get("https://coinmarketcap.com/exchanges/")
            
            # Wait for page to load
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "table.cmc-table"))
            )
            
            # Log success
            logger.debug("Successfully navigated between pages")
        except Exception as e:
            logger.error(f"Error navigating between pages: {e}")
