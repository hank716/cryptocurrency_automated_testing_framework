from locust import HttpUser, task, between
import logging
import random

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class CryptocurrencyAPIUser(HttpUser):
    """
    Locust user class for testing cryptocurrency API endpoints.
    
    This class simulates user behavior for API load testing,
    focusing on cryptocurrency-related endpoints.
    """
    
    # Wait time between tasks (1-5 seconds)
    wait_time = between(1, 5)
    
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
        logger.info("API user session started")
    
    @task(3)
    def get_cryptocurrency_listings(self):
        """
        Task to get cryptocurrency listings.
        
        This is a high-frequency task (weight: 3).
        """
        # Random limit between 10 and 100
        limit = random.randint(10, 100)
        
        # Random currency for conversion
        currencies = ["USD", "EUR", "JPY", "KRW", "BTC"]
        convert = random.choice(currencies)
        
        # Make request
        with self.client.get(
            "/v1/cryptocurrency/listings/latest",
            params={"limit": limit, "convert": convert},
            name="/v1/cryptocurrency/listings/latest",
            catch_response=True
        ) as response:
            # Validate response
            if response.status_code == 200:
                # Parse response JSON
                data = response.json()
                
                # Verify response structure
                if 'status' in data and 'data' in data:
                    # Verify status
                    if data['status']['error_code'] == 0:
                        response.success()
                        logger.debug(f"Successfully retrieved {len(data['data'])} cryptocurrencies")
                    else:
                        response.failure(f"API error: {data['status']['error_message']}")
                else:
                    response.failure("Invalid response structure")
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
        
        # Random selection of 1-3 symbols
        count = random.randint(1, 3)
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
                # Parse response JSON
                data = response.json()
                
                # Verify response structure
                if 'status' in data and 'data' in data:
                    # Verify status
                    if data['status']['error_code'] == 0:
                        response.success()
                        logger.debug(f"Successfully retrieved info for {symbol_string}")
                    else:
                        response.failure(f"API error: {data['status']['error_message']}")
                else:
                    response.failure("Invalid response structure")
            else:
                response.failure(f"Unexpected status code: {response.status_code}")
    
    @task(1)
    def get_cryptocurrency_quotes(self):
        """
        Task to get cryptocurrency quotes.
        
        This is a low-frequency task (weight: 1).
        """
        # Common cryptocurrency IDs
        ids = ["1", "1027", "52", "2010", "5426"]  # BTC, ETH, XRP, ADA, SOL
        
        # Random selection of 1-5 IDs
        count = random.randint(1, 5)
        selected_ids = random.sample(ids, count)
        id_string = ",".join(selected_ids)
        
        # Random currency for conversion
        currencies = ["USD", "EUR", "JPY", "KRW", "BTC"]
        convert = random.choice(currencies)
        
        # Make request
        with self.client.get(
            "/v2/cryptocurrency/quotes/latest",
            params={"id": id_string, "convert": convert},
            name="/v2/cryptocurrency/quotes/latest",
            catch_response=True
        ) as response:
            # Validate response
            if response.status_code == 200:
                # Parse response JSON
                data = response.json()
                
                # Verify response structure
                if 'status' in data and 'data' in data:
                    # Verify status
                    if data['status']['error_code'] == 0:
                        response.success()
                        logger.debug(f"Successfully retrieved quotes for {id_string}")
                    else:
                        response.failure(f"API error: {data['status']['error_message']}")
                else:
                    response.failure("Invalid response structure")
            else:
                response.failure(f"Unexpected status code: {response.status_code}")
    
    @task(1)
    def get_exchange_listings(self):
        """
        Task to get exchange listings.
        
        This is a low-frequency task (weight: 1).
        """
        # Random limit between 10 and 50
        limit = random.randint(10, 50)
        
        # Make request
        with self.client.get(
            "/v1/exchange/listings/latest",
            params={"limit": limit},
            name="/v1/exchange/listings/latest",
            catch_response=True
        ) as response:
            # Validate response
            if response.status_code == 200:
                # Parse response JSON
                data = response.json()
                
                # Verify response structure
                if 'status' in data and 'data' in data:
                    # Verify status
                    if data['status']['error_code'] == 0:
                        response.success()
                        logger.debug(f"Successfully retrieved {len(data['data'])} exchanges")
                    else:
                        response.failure(f"API error: {data['status']['error_message']}")
                else:
                    response.failure("Invalid response structure")
            else:
                response.failure(f"Unexpected status code: {response.status_code}")
