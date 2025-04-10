import pytest
import logging
import time
from typing import Dict, Any

from utils.api_client import ApiClient

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


@pytest.mark.api
class TestCryptocurrency:
    """
    Test suite for cryptocurrency API endpoints.
    
    This class contains tests for cryptocurrency-related API endpoints
    such as listings, details, and market data.
    """
    
    def test_get_cryptocurrency_listings(self, api_client: ApiClient):
        """
        Test getting cryptocurrency listings.
        
        Args:
            api_client: API client fixture
        """
        # Get cryptocurrency listings
        response = api_client.get_cryptocurrency_listings(limit=10)
        
        # Verify response
        assert response.status_code == 200
        
        # Parse response JSON
        data = response.json()
        
        # Verify response structure
        assert 'status' in data
        assert 'data' in data
        
        # Verify status
        assert data['status']['error_code'] == 0
        assert data['status']['error_message'] is None
        
        # Verify data
        assert isinstance(data['data'], list)
        assert len(data['data']) <= 10
        
        # Verify first cryptocurrency
        if data['data']:
            crypto = data['data'][0]
            assert 'id' in crypto
            assert 'name' in crypto
            assert 'symbol' in crypto
            assert 'quote' in crypto
            
            # Verify quote
            assert 'USD' in crypto['quote']
            assert 'price' in crypto['quote']['USD']
            assert 'market_cap' in crypto['quote']['USD']
            assert 'volume_24h' in crypto['quote']['USD']
    
    def test_get_cryptocurrency_info(self, api_client: ApiClient):
        """
        Test getting cryptocurrency information.
        
        Args:
            api_client: API client fixture
        """
        # Get cryptocurrency information for Bitcoin
        response = api_client.get_cryptocurrency_info('BTC')
        
        # Verify response
        assert response.status_code == 200
        
        # Parse response JSON
        data = response.json()
        
        # Verify response structure
        assert 'status' in data
        assert 'data' in data
        
        # Verify status
        assert data['status']['error_code'] == 0
        assert data['status']['error_message'] is None
        
        # Verify data
        assert isinstance(data['data'], dict)
        
        # Verify Bitcoin data
        btc_data = None
        for symbol, crypto_data in data['data'].items():
            if symbol == 'BTC':
                btc_data = crypto_data
                break
        
        assert btc_data is not None
        assert 'id' in btc_data
        assert 'name' in btc_data
        assert 'symbol' in btc_data
        assert btc_data['name'] == 'Bitcoin'
        assert btc_data['symbol'] == 'BTC'
    
    @pytest.mark.parametrize("symbol", ["BTC", "ETH", "XRP"])
    def test_get_multiple_cryptocurrencies(self, api_client: ApiClient, symbol: str):
        """
        Test getting information for multiple cryptocurrencies.
        
        Args:
            api_client: API client fixture
            symbol: Cryptocurrency symbol
        """
        # Get cryptocurrency information
        response = api_client.get_cryptocurrency_info(symbol)
        
        # Verify response
        assert response.status_code == 200
        
        # Parse response JSON
        data = response.json()
        
        # Verify response structure
        assert 'status' in data
        assert 'data' in data
        
        # Verify status
        assert data['status']['error_code'] == 0
        assert data['status']['error_message'] is None
        
        # Verify data
        assert isinstance(data['data'], dict)
        
        # Verify cryptocurrency data
        crypto_data = None
        for s, cd in data['data'].items():
            if s == symbol:
                crypto_data = cd
                break
        
        assert crypto_data is not None
        assert 'id' in crypto_data
        assert 'name' in crypto_data
        assert 'symbol' in crypto_data
        assert crypto_data['symbol'] == symbol
    
    @pytest.mark.slow
    def test_get_all_cryptocurrencies(self, api_client: ApiClient):
        """
        Test getting all cryptocurrencies.
        
        Args:
            api_client: API client fixture
        """
        # Get all cryptocurrencies (limit=5000)
        response = api_client.get_cryptocurrency_listings(limit=5000)
        
        # Verify response
        assert response.status_code == 200
        
        # Parse response JSON
        data = response.json()
        
        # Verify response structure
        assert 'status' in data
        assert 'data' in data
        
        # Verify status
        assert data['status']['error_code'] == 0
        assert data['status']['error_message'] is None
        
        # Verify data
        assert isinstance(data['data'], list)
        
        # Log the number of cryptocurrencies
        logger.info(f"Number of cryptocurrencies: {len(data['data'])}")
    
    @pytest.mark.performance
    def test_api_response_time(self, api_client: ApiClient):
        """
        Test API response time.
        
        Args:
            api_client: API client fixture
        """
        # Measure response time for getting cryptocurrency listings
        start_time = time.time()
        response = api_client.get_cryptocurrency_listings(limit=10)
        end_time = time.time()
        
        # Calculate response time
        response_time = end_time - start_time
        
        # Verify response
        assert response.status_code == 200
        
        # Verify response time is within acceptable range (less than 2 seconds)
        assert response_time < 2.0
        
        # Log response time
        logger.info(f"API response time: {response_time:.2f} seconds")
