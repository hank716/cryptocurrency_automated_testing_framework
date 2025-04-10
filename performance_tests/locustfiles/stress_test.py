from locust import HttpUser, task, between
import logging
import random

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class StressTestUser(HttpUser):
    """
    Locust user class for stress testing cryptocurrency API endpoints.
    
    This class simulates high-load user behavior for stress testing,
    focusing on rapid and concurrent API requests.
    """
    
    # Very short wait time between tasks (0.1-1 seconds)
    wait_time = between(0.1, 1)
    
    def on_start(self):
        """
        Initialize user session.
        """
        # Set API key header if needed
        self.client.headers = {
            'Accept': 'application/json',
            'User-Agent': 'Crypto-QA-Framework/1.0',
            'X-CMC_PRO_API_KEY': 'your-api-key-here'  # Replace with actual API key
        }
        logger.info("Stress test user session started")
    
    @task(5)
    def get_cryptocurrency_listings(self):
        """
        Task to get cryptocurrency listings.
        
        This is a very high-frequency task (weight: 5).
        """
        # Random limit between 10 and 200
        limit = random.randint(10, 200)
        
        # Make request
        with self.client.get(
            "/v1/cryptocurrency/listings/latest",
            params={"limit": limit},
            name="/v1/cryptocurrency/listings/latest",
            catch_response=True
        ) as response:
            # Validate response
            if response.status_code == 200:
                response.success()
            else:
                response.failure(f"Unexpected status code: {response.status_code}")
    
    @task(3)
    def get_cryptocurrency_quotes(self):
        """
        Task to get cryptocurrency quotes.
        
        This is a high-frequency task (weight: 3).
        """
        # Common cryptocurrency IDs
        ids = ["1", "1027", "52", "2010", "5426", "6636", "74", "5994", "3408", "7083"]
        
        # Random selection of 1-10 IDs
        count = random.randint(1, 10)
        selected_ids = random.sample(ids, count)
        id_string = ",".join(selected_ids)
        
        # Make request
        with self.client.get(
            "/v2/cryptocurrency/quotes/latest",
            params={"id": id_string},
            name="/v2/cryptocurrency/quotes/latest",
            catch_response=True
        ) as response:
            # Validate response
            if response.status_code == 200:
                response.success()
            else:
                response.failure(f"Unexpected status code: {response.status_code}")
    
    @task(2)
    def get_cryptocurrency_info(self):
        """
        Task to get cryptocurrency information.
        
        This is a medium-frequency task (weight: 2).
        """
        # Common cryptocurrency symbols
        symbols = ["BTC", "ETH", "XRP", "ADA", "SOL", "DOT", "DOGE", "AVAX", "LINK", "MATIC"]
        
        # Random selection of 1-5 symbols
        count = random.randint(1, 5)
        selected_symbols = random.sample(symbols, count)
        symbol_string = ",".join(selected_symbols)
        
        # Make request
        with self.client.get(
            "/v2/cryptocurrency/info",
            params={"symbol": symbol_string},
            name="/v2/cryptocurrency/info",
            catch_response=True
        ) as response:
            # Validate response
            if response.status_code == 200:
                response.success()
            else:
                response.failure(f"Unexpected status code: {response.status_code}")
    
    @task(2)
    def get_exchange_listings(self):
        """
        Task to get exchange listings.
        
        This is a medium-frequency task (weight: 2).
        """
        # Random limit between 10 and 100
        limit = random.randint(10, 100)
        
        # Make request
        with self.client.get(
            "/v1/exchange/listings/latest",
            params={"limit": limit},
            name="/v1/exchange/listings/latest",
            catch_response=True
        ) as response:
            # Validate response
            if response.status_code == 200:
                response.success()
            else:
                response.failure(f"Unexpected status code: {response.status_code}")
    
    @task(1)
    def get_global_metrics(self):
        """
        Task to get global cryptocurrency metrics.
        
        This is a low-frequency task (weight: 1).
        """
        # Make request
        with self.client.get(
            "/v1/global-metrics/quotes/latest",
            name="/v1/global-metrics/quotes/latest",
            catch_response=True
        ) as response:
            # Validate response
            if response.status_code == 200:
                response.success()
            else:
                response.failure(f"Unexpected status code: {response.status_code}")
    
    @task(1)
    def get_exchange_info(self):
        """
        Task to get exchange information.
        
        This is a low-frequency task (weight: 1).
        """
        # Common exchange IDs
        ids = ["270", "294", "73", "102", "37"]  # Binance, Coinbase, Kraken, etc.
        
        # Random selection of 1-3 IDs
        count = random.randint(1, 3)
        selected_ids = random.sample(ids, count)
        id_string = ",".join(selected_ids)
        
        # Make request
        with self.client.get(
            "/v1/exchange/info",
            params={"id": id_string},
            name="/v1/exchange/info",
            catch_response=True
        ) as response:
            # Validate response
            if response.status_code == 200:
                response.success()
            else:
                response.failure(f"Unexpected status code: {response.status_code}")
