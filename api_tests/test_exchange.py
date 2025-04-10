import pytest
import logging
from typing import Dict, Any

from utils.api_client import ApiClient

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


@pytest.mark.api
class TestExchange:
    """
    Test suite for exchange API endpoints.
    
    This class contains tests for exchange-related API endpoints
    such as listings, details, and market data.
    """
    
    def test_get_exchange_listings(self, api_client: ApiClient):
        """
        Test getting exchange listings.
        
        Args:
            api_client: API client fixture
        """
        # Get exchange listings
        response = api_client.get_exchange_listings(limit=10)
        
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
        
        # Verify first exchange
        if data['data']:
            exchange = data['data'][0]
            assert 'id' in exchange
            assert 'name' in exchange
            assert 'slug' in exchange
            assert 'quote' in exchange
            
            # Verify quote
            assert 'USD' in exchange['quote']
            assert 'volume_24h' in exchange['quote']['USD']
    
    @pytest.mark.parametrize("exchange_id", [1, 2, 3])
    def test_get_exchange_details(self, api_client: ApiClient, exchange_id: int):
        """
        Test getting exchange details.
        
        Args:
            api_client: API client fixture
            exchange_id: Exchange ID
        """
        # Get exchange details
        endpoint = f'/v1/exchange/info'
        params = {'id': exchange_id}
        response = api_client.get(endpoint, params)
        
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
        
        # Verify exchange data
        exchange_data = data['data'].get(str(exchange_id))
        assert exchange_data is not None
        assert 'id' in exchange_data
        assert 'name' in exchange_data
        assert 'slug' in exchange_data
        assert int(exchange_data['id']) == exchange_id
    
    def test_get_exchange_market_pairs(self, api_client: ApiClient):
        """
        Test getting exchange market pairs.
        
        Args:
            api_client: API client fixture
        """
        # Get market pairs for Binance (ID: 270)
        endpoint = '/v1/exchange/market-pairs/latest'
        params = {'id': 270, 'limit': 10}
        response = api_client.get(endpoint, params)
        
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
        assert 'id' in data['data']
        assert 'name' in data['data']
        assert 'slug' in data['data']
        assert 'market_pairs' in data['data']
        
        # Verify market pairs
        assert isinstance(data['data']['market_pairs'], list)
        assert len(data['data']['market_pairs']) <= 10
        
        # Verify first market pair
        if data['data']['market_pairs']:
            market_pair = data['data']['market_pairs'][0]
            assert 'market_pair' in market_pair
            assert 'base_currency' in market_pair
            assert 'quote_currency' in market_pair
    
    def test_get_exchange_quotes(self, api_client: ApiClient):
        """
        Test getting exchange quotes.
        
        Args:
            api_client: API client fixture
        """
        # Get quotes for multiple exchanges
        endpoint = '/v1/exchange/quotes/latest'
        params = {'id': '270,271,294', 'convert': 'USD'}  # Binance, Coinbase, Kraken
        response = api_client.get(endpoint, params)
        
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
        assert len(data['data']) <= 3
        
        # Verify exchange data
        for exchange_id, exchange_data in data['data'].items():
            assert 'id' in exchange_data
            assert 'name' in exchange_data
            assert 'slug' in exchange_data
            assert 'quote' in exchange_data
            assert 'USD' in exchange_data['quote']
            assert 'volume_24h' in exchange_data['quote']['USD']
    
    @pytest.mark.slow
    def test_get_all_exchanges(self, api_client: ApiClient):
        """
        Test getting all exchanges.
        
        Args:
            api_client: API client fixture
        """
        # Get all exchanges (limit=500)
        response = api_client.get_exchange_listings(limit=500)
        
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
        
        # Log the number of exchanges
        logger.info(f"Number of exchanges: {len(data['data'])}")
