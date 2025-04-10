import pytest
import logging
import time
import statistics
from typing import Dict, Any, List

from utils.api_client import ApiClient

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


@pytest.mark.performance
class TestPerformance:
    """
    Test suite for API performance testing.
    
    This class contains tests for measuring API performance metrics
    such as response time, throughput, and consistency.
    """
    
    def test_api_response_time(self, api_client: ApiClient):
        """
        Test API response time for cryptocurrency listings.
        
        Args:
            api_client: API client fixture
        """
        # Number of requests to make
        num_requests = 5
        response_times = []
        
        # Make multiple requests and measure response time
        for i in range(num_requests):
            start_time = time.time()
            response = api_client.get_cryptocurrency_listings(limit=10)
            end_time = time.time()
            
            # Calculate response time
            response_time = end_time - start_time
            response_times.append(response_time)
            
            # Verify response
            assert response.status_code == 200
            
            # Log response time
            logger.info(f"Request {i+1}: Response time = {response_time:.2f} seconds")
            
            # Add a small delay between requests
            time.sleep(1)
        
        # Calculate statistics
        avg_response_time = statistics.mean(response_times)
        min_response_time = min(response_times)
        max_response_time = max(response_times)
        
        # Log statistics
        logger.info(f"Average response time: {avg_response_time:.2f} seconds")
        logger.info(f"Minimum response time: {min_response_time:.2f} seconds")
        logger.info(f"Maximum response time: {max_response_time:.2f} seconds")
        
        # Verify average response time is within acceptable range (less than 2 seconds)
        assert avg_response_time < 2.0
    
    def test_api_throughput(self, api_client: ApiClient):
        """
        Test API throughput for cryptocurrency listings.
        
        Args:
            api_client: API client fixture
        """
        # Number of requests to make
        num_requests = 10
        
        # Start time for all requests
        start_time = time.time()
        
        # Make multiple requests
        for i in range(num_requests):
            response = api_client.get_cryptocurrency_listings(limit=10)
            
            # Verify response
            assert response.status_code == 200
        
        # End time for all requests
        end_time = time.time()
        
        # Calculate total time and throughput
        total_time = end_time - start_time
        throughput = num_requests / total_time
        
        # Log throughput
        logger.info(f"Total time for {num_requests} requests: {total_time:.2f} seconds")
        logger.info(f"Throughput: {throughput:.2f} requests per second")
        
        # Verify throughput is within acceptable range (at least 0.5 requests per second)
        assert throughput >= 0.5
    
    def test_api_consistency(self, api_client: ApiClient):
        """
        Test API response consistency for cryptocurrency listings.
        
        Args:
            api_client: API client fixture
        """
        # Number of requests to make
        num_requests = 3
        responses = []
        
        # Make multiple requests
        for i in range(num_requests):
            response = api_client.get_cryptocurrency_listings(limit=10)
            
            # Verify response
            assert response.status_code == 200
            
            # Parse response JSON
            data = response.json()
            
            # Store response data
            responses.append(data)
            
            # Add a small delay between requests
            time.sleep(1)
        
        # Verify response consistency
        for i in range(1, num_requests):
            # Verify status
            assert responses[i]['status']['error_code'] == responses[0]['status']['error_code']
            
            # Verify data structure
            assert len(responses[i]['data']) == len(responses[0]['data'])
            
            # Verify cryptocurrency IDs
            for j in range(len(responses[i]['data'])):
                assert responses[i]['data'][j]['id'] == responses[0]['data'][j]['id']
                assert responses[i]['data'][j]['name'] == responses[0]['data'][j]['name']
                assert responses[i]['data'][j]['symbol'] == responses[0]['data'][j]['symbol']
    
    def test_api_concurrent_requests(self, api_client: ApiClient):
        """
        Test API handling of concurrent requests.
        
        Args:
            api_client: API client fixture
        """
        import concurrent.futures
        
        # Number of concurrent requests
        num_concurrent = 5
        
        # Function to make a request
        def make_request():
            start_time = time.time()
            response = api_client.get_cryptocurrency_listings(limit=10)
            end_time = time.time()
            
            # Calculate response time
            response_time = end_time - start_time
            
            # Verify response
            assert response.status_code == 200
            
            return response_time
        
        # Make concurrent requests
        with concurrent.futures.ThreadPoolExecutor(max_workers=num_concurrent) as executor:
            future_to_request = {executor.submit(make_request): i for i in range(num_concurrent)}
            response_times = []
            
            for future in concurrent.futures.as_completed(future_to_request):
                request_id = future_to_request[future]
                try:
                    response_time = future.result()
                    response_times.append(response_time)
                    logger.info(f"Request {request_id}: Response time = {response_time:.2f} seconds")
                except Exception as e:
                    logger.error(f"Request {request_id} generated an exception: {e}")
        
        # Calculate statistics
        avg_response_time = statistics.mean(response_times)
        min_response_time = min(response_times)
        max_response_time = max(response_times)
        
        # Log statistics
        logger.info(f"Average response time (concurrent): {avg_response_time:.2f} seconds")
        logger.info(f"Minimum response time (concurrent): {min_response_time:.2f} seconds")
        logger.info(f"Maximum response time (concurrent): {max_response_time:.2f} seconds")
        
        # Verify average response time is within acceptable range (less than 3 seconds for concurrent requests)
        assert avg_response_time < 3.0
    
    @pytest.mark.slow
    def test_api_rate_limiting(self, api_client: ApiClient):
        """
        Test API rate limiting.
        
        Args:
            api_client: API client fixture
        """
        # Number of requests to make
        num_requests = 30
        response_times = []
        status_codes = []
        
        # Make multiple requests in quick succession
        for i in range(num_requests):
            start_time = time.time()
            try:
                response = api_client.get_cryptocurrency_listings(limit=10)
                status_codes.append(response.status_code)
            except Exception as e:
                logger.warning(f"Request {i+1} failed: {e}")
                status_codes.append(429)  # Assume rate limit exceeded
            end_time = time.time()
            
            # Calculate response time
            response_time = end_time - start_time
            response_times.append(response_time)
            
            # Log response time and status code
            logger.info(f"Request {i+1}: Response time = {response_time:.2f} seconds, Status code = {status_codes[-1]}")
        
        # Count status codes
        success_count = status_codes.count(200)
        rate_limit_count = status_codes.count(429)
        
        # Log statistics
        logger.info(f"Successful requests: {success_count}/{num_requests}")
        logger.info(f"Rate limited requests: {rate_limit_count}/{num_requests}")
        
        # Note: We don't assert on rate limiting behavior as it depends on the API's rate limits
        # This test is for observational purposes
