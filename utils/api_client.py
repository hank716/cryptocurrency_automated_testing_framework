import requests
import time
import logging
from typing import Dict, Any, Optional, Union, Callable
from functools import wraps

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def retry(max_attempts: int = 3, delay: int = 1, backoff: int = 2, 
          exceptions: tuple = (requests.exceptions.RequestException,)):
    """
    Retry decorator for API calls.
    
    Args:
        max_attempts: Maximum number of retry attempts
        delay: Initial delay between retries in seconds
        backoff: Backoff multiplier
        exceptions: Tuple of exceptions to catch and retry
        
    Returns:
        Decorated function
    """
    def decorator(func: Callable):
        @wraps(func)
        def wrapper(*args, **kwargs):
            attempt = 0
            current_delay = delay
            
            while attempt < max_attempts:
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    attempt += 1
                    if attempt == max_attempts:
                        logger.error(f"Failed after {max_attempts} attempts: {e}")
                        raise
                    
                    logger.warning(f"Attempt {attempt} failed: {e}. Retrying in {current_delay}s...")
                    time.sleep(current_delay)
                    current_delay *= backoff
        
        return wrapper
    return decorator


class ApiClient:
    """
    API Client for cryptocurrency API interactions.
    
    This class provides methods for making API requests to cryptocurrency
    endpoints with retry capabilities, error handling, and logging.
    """
    
    def __init__(self, base_url: str, api_key: Optional[str] = None, 
                 timeout: int = 30, retry_count: int = 3):
        """
        Initialize the API client.
        
        Args:
            base_url: Base URL for API requests
            api_key: API key for authentication
            timeout: Request timeout in seconds
            retry_count: Number of retry attempts for failed requests
        """
        self.base_url = base_url
        self.api_key = api_key
        self.timeout = timeout
        self.retry_count = retry_count
        self.session = requests.Session()
        
        # Set default headers
        self.session.headers.update({
            'Accept': 'application/json',
            'User-Agent': 'Crypto-QA-Framework/1.0'
        })
        
        if api_key:
            self.session.headers.update({'X-CMC_PRO_API_KEY': api_key})
    
    @retry(max_attempts=3)
    def get(self, endpoint: str, params: Optional[Dict[str, Any]] = None) -> requests.Response:
        """
        Make a GET request to the API.
        
        Args:
            endpoint: API endpoint path
            params: Query parameters
            
        Returns:
            Response object
        """
        url = f"{self.base_url}{endpoint}"
        logger.info(f"GET request to {url}")
        
        response = self.session.get(
            url,
            params=params,
            timeout=self.timeout
        )
        
        logger.info(f"Response status: {response.status_code}")
        response.raise_for_status()
        return response
    
    @retry(max_attempts=3)
    def post(self, endpoint: str, data: Optional[Dict[str, Any]] = None, 
             json_data: Optional[Dict[str, Any]] = None) -> requests.Response:
        """
        Make a POST request to the API.
        
        Args:
            endpoint: API endpoint path
            data: Form data
            json_data: JSON data
            
        Returns:
            Response object
        """
        url = f"{self.base_url}{endpoint}"
        logger.info(f"POST request to {url}")
        
        response = self.session.post(
            url,
            data=data,
            json=json_data,
            timeout=self.timeout
        )
        
        logger.info(f"Response status: {response.status_code}")
        response.raise_for_status()
        return response
    
    @retry(max_attempts=3)
    def put(self, endpoint: str, data: Optional[Dict[str, Any]] = None, 
            json_data: Optional[Dict[str, Any]] = None) -> requests.Response:
        """
        Make a PUT request to the API.
        
        Args:
            endpoint: API endpoint path
            data: Form data
            json_data: JSON data
            
        Returns:
            Response object
        """
        url = f"{self.base_url}{endpoint}"
        logger.info(f"PUT request to {url}")
        
        response = self.session.put(
            url,
            data=data,
            json=json_data,
            timeout=self.timeout
        )
        
        logger.info(f"Response status: {response.status_code}")
        response.raise_for_status()
        return response
    
    @retry(max_attempts=3)
    def delete(self, endpoint: str, params: Optional[Dict[str, Any]] = None) -> requests.Response:
        """
        Make a DELETE request to the API.
        
        Args:
            endpoint: API endpoint path
            params: Query parameters
            
        Returns:
            Response object
        """
        url = f"{self.base_url}{endpoint}"
        logger.info(f"DELETE request to {url}")
        
        response = self.session.delete(
            url,
            params=params,
            timeout=self.timeout
        )
        
        logger.info(f"Response status: {response.status_code}")
        response.raise_for_status()
        return response
    
    def get_cryptocurrency_listings(self, limit: int = 100, 
                                   convert: str = 'USD') -> requests.Response:
        """
        Get cryptocurrency listings.
        
        Args:
            limit: Number of results to return
            convert: Currency to convert prices to
            
        Returns:
            Response object
        """
        endpoint = '/v1/cryptocurrency/listings/latest'
        params = {
            'limit': limit,
            'convert': convert
        }
        
        return self.get(endpoint, params)
    
    def get_cryptocurrency_info(self, symbol: str) -> requests.Response:
        """
        Get cryptocurrency information by symbol.
        
        Args:
            symbol: Cryptocurrency symbol (e.g., BTC, ETH)
            
        Returns:
            Response object
        """
        endpoint = '/v2/cryptocurrency/info'
        params = {
            'symbol': symbol
        }
        
        return self.get(endpoint, params)
    
    def get_exchange_listings(self, limit: int = 100) -> requests.Response:
        """
        Get exchange listings.
        
        Args:
            limit: Number of results to return
            
        Returns:
            Response object
        """
        endpoint = '/v1/exchange/listings/latest'
        params = {
            'limit': limit
        }
        
        return self.get(endpoint, params)
    
    def close(self) -> None:
        """Close the session."""
        self.session.close()
