from locust import HttpUser, task, between
import logging
import random
import time

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class StabilityTestUser(HttpUser):
    """
    Locust user class for stability testing cryptocurrency API endpoints.
    
    This class simulates long-running user behavior for stability testing,
    focusing on consistent API usage over extended periods.
    """
    
    # Moderate wait time between tasks (5-15 seconds)
    wait_time = between(5, 15)
    
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
        # Track session start time
        self.start_time = time.time()
        # Initialize counters
        self.request_count = 0
        self.success_count = 0
        self.failure_count = 0
        
        logger.info("Stability test user session started")
    
    def on_stop(self):
        """
        Clean up resources and log statistics when the test stops.
        """
        # Calculate session duration
        duration = time.time() - self.start_time
        
        # Log statistics
        logger.info(f"Stability test user session ended after {duration:.2f} seconds")
        logger.info(f"Total requests: {self.request_count}")
        logger.info(f"Successful requests: {self.success_count}")
        logger.info(f"Failed requests: {self.failure_count}")
        
        if self.request_count > 0:
            success_rate = (self.success_count / self.request_count) * 100
            logger.info(f"Success rate: {success_rate:.2f}%")
    
    def track_request(self, success):
        """
        Track request outcome.
        
        Args:
            success: Whether the request was successful
        """
        self.request_count += 1
        if success:
            self.success_count += 1
        else:
            self.failure_count += 1
    
    @task(3)
    def get_cryptocurrency_listings(self):
        """
        Task to get cryptocurrency listings.
        
        This is a high-frequency task (weight: 3).
        """
        # Random limit between 10 and 100
        limit = random.randint(10, 100)
        
        # Make request
        with self.client.get(
            "/v1/cryptocurrency/listings/latest",
            params={"limit": limit},
            name="/v1/cryptocurrency/listings/latest",
            catch_response=True
        ) as response:
            # Validate response
            if response.status_code == 200:
                # Parse response JSON
                try:
                    data = response.json()
                    
                    # Verify response structure
                    if 'status' in data and 'data' in data:
                        # Verify status
                        if data['status']['error_code'] == 0:
                            response.success()
                            self.track_request(True)
                            logger.debug(f"Successfully retrieved {len(data['data'])} cryptocurrencies")
                        else:
                            response.failure(f"API error: {data['status']['error_message']}")
                            self.track_request(False)
                    else:
                        response.failure("Invalid response structure")
                        self.track_request(False)
                except ValueError:
                    response.failure("Invalid JSON response")
                    self.track_request(False)
            else:
                response.failure(f"Unexpected status code: {response.status_code}")
                self.track_request(False)
    
    @task(2)
    def get_cryptocurrency_quotes(self):
        """
        Task to get cryptocurrency quotes.
        
        This is a medium-frequency task (weight: 2).
        """
        # Common cryptocurrency IDs
        ids = ["1", "1027", "52", "2010", "5426"]  # BTC, ETH, XRP, ADA, SOL
        
        # Random selection of 1-5 IDs
        count = random.randint(1, 5)
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
                try:
                    data = response.json()
                    if 'status' in data and 'data' in data:
                        if data['status']['error_code'] == 0:
                            response.success()
                            self.track_request(True)
                        else:
                            response.failure(f"API error: {data['status']['error_message']}")
                            self.track_request(False)
                    else:
                        response.failure("Invalid response structure")
                        self.track_request(False)
                except ValueError:
                    response.failure("Invalid JSON response")
                    self.track_request(False)
            else:
                response.failure(f"Unexpected status code: {response.status_code}")
                self.track_request(False)
    
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
                try:
                    data = response.json()
                    if 'status' in data and 'data' in data:
                        if data['status']['error_code'] == 0:
                            response.success()
                            self.track_request(True)
                        else:
                            response.failure(f"API error: {data['status']['error_message']}")
                            self.track_request(False)
                    else:
                        response.failure("Invalid response structure")
                        self.track_request(False)
                except ValueError:
                    response.failure("Invalid JSON response")
                    self.track_request(False)
            else:
                response.failure(f"Unexpected status code: {response.status_code}")
                self.track_request(False)
    
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
                try:
                    data = response.json()
                    if 'status' in data and 'data' in data:
                        if data['status']['error_code'] == 0:
                            response.success()
                            self.track_request(True)
                        else:
                            response.failure(f"API error: {data['status']['error_message']}")
                            self.track_request(False)
                    else:
                        response.failure("Invalid response structure")
                        self.track_request(False)
                except ValueError:
                    response.failure("Invalid JSON response")
                    self.track_request(False)
            else:
                response.failure(f"Unexpected status code: {response.status_code}")
                self.track_request(False)
