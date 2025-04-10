import random
import string
import datetime
from typing import List, Dict, Any, Optional, Union


class DataGenerator:
    """
    Test data generator for cryptocurrency testing.
    
    This class provides methods for generating test data such as
    cryptocurrency information, exchange data, and market data.
    """
    
    @staticmethod
    def generate_cryptocurrency(count: int = 1) -> List[Dict[str, Any]]:
        """
        Generate cryptocurrency test data.
        
        Args:
            count: Number of cryptocurrency records to generate
            
        Returns:
            List of cryptocurrency dictionaries
        """
        cryptocurrencies = []
        
        # Common cryptocurrency names and symbols
        names = ["Bitcoin", "Ethereum", "Ripple", "Cardano", "Solana", 
                "Polkadot", "Dogecoin", "Avalanche", "Chainlink", "Polygon"]
        symbols = ["BTC", "ETH", "XRP", "ADA", "SOL", 
                  "DOT", "DOGE", "AVAX", "LINK", "MATIC"]
        
        for i in range(count):
            # Use predefined names if available, otherwise generate random ones
            if i < len(names):
                name = names[i]
                symbol = symbols[i]
            else:
                name = f"Crypto{i+1}"
                symbol = ''.join(random.choices(string.ascii_uppercase, k=3))
            
            # Generate random price between $0.01 and $100,000
            price = round(random.uniform(0.01, 100000), 2)
            
            # Generate random market cap between $1M and $1T
            market_cap = random.randint(1000000, 1000000000000)
            
            # Generate random 24h volume between $100K and $50B
            volume_24h = random.randint(100000, 50000000000)
            
            # Generate random percent change between -20% and +20%
            percent_change_24h = round(random.uniform(-20, 20), 2)
            
            # Create cryptocurrency dictionary
            crypto = {
                "id": i + 1,
                "name": name,
                "symbol": symbol,
                "price_usd": price,
                "market_cap_usd": market_cap,
                "volume_24h_usd": volume_24h,
                "percent_change_24h": percent_change_24h,
                "last_updated": datetime.datetime.now().isoformat()
            }
            
            cryptocurrencies.append(crypto)
        
        return cryptocurrencies
    
    @staticmethod
    def generate_exchange(count: int = 1) -> List[Dict[str, Any]]:
        """
        Generate exchange test data.
        
        Args:
            count: Number of exchange records to generate
            
        Returns:
            List of exchange dictionaries
        """
        exchanges = []
        
        # Common exchange names
        names = ["Binance", "Coinbase", "Kraken", "FTX", "Huobi", 
                "KuCoin", "Bitfinex", "Bitstamp", "Gemini", "OKX"]
        
        for i in range(count):
            # Use predefined names if available, otherwise generate random ones
            if i < len(names):
                name = names[i]
            else:
                name = f"Exchange{i+1}"
            
            # Generate random 24h volume between $10M and $10B
            volume_24h = random.randint(10000000, 10000000000)
            
            # Generate random number of markets between 100 and 2000
            markets_count = random.randint(100, 2000)
            
            # Generate random number of coins between 50 and 500
            coins_count = random.randint(50, 500)
            
            # Create exchange dictionary
            exchange = {
                "id": i + 1,
                "name": name,
                "volume_24h_usd": volume_24h,
                "markets_count": markets_count,
                "coins_count": coins_count,
                "last_updated": datetime.datetime.now().isoformat()
            }
            
            exchanges.append(exchange)
        
        return exchanges
    
    @staticmethod
    def generate_market_data(crypto_count: int = 5, exchange_count: int = 3) -> List[Dict[str, Any]]:
        """
        Generate market data for cryptocurrency-exchange pairs.
        
        Args:
            crypto_count: Number of cryptocurrencies
            exchange_count: Number of exchanges
            
        Returns:
            List of market data dictionaries
        """
        market_data = []
        
        # Generate cryptocurrencies and exchanges
        cryptocurrencies = DataGenerator.generate_cryptocurrency(crypto_count)
        exchanges = DataGenerator.generate_exchange(exchange_count)
        
        # Create market data for each crypto-exchange pair
        for crypto in cryptocurrencies:
            for exchange in exchanges:
                # Generate slightly different price for each exchange (±2%)
                price = crypto["price_usd"] * random.uniform(0.98, 1.02)
                
                # Generate random volume for this pair
                volume = random.randint(
                    int(crypto["volume_24h_usd"] * 0.01),  # 1% of total volume
                    int(crypto["volume_24h_usd"] * 0.3)    # 30% of total volume
                )
                
                # Create market data dictionary
                data = {
                    "cryptocurrency_id": crypto["id"],
                    "cryptocurrency_symbol": crypto["symbol"],
                    "exchange_id": exchange["id"],
                    "exchange_name": exchange["name"],
                    "price_usd": round(price, 2),
                    "volume_24h_usd": volume,
                    "last_updated": datetime.datetime.now().isoformat()
                }
                
                market_data.append(data)
        
        return market_data
    
    @staticmethod
    def generate_api_response(data_type: str, count: int = 5) -> Dict[str, Any]:
        """
        Generate mock API response with the specified data type.
        
        Args:
            data_type: Type of data to generate ('cryptocurrency', 'exchange', or 'market')
            count: Number of records to generate
            
        Returns:
            Dictionary mimicking API response format
        """
        if data_type == 'cryptocurrency':
            data = DataGenerator.generate_cryptocurrency(count)
        elif data_type == 'exchange':
            data = DataGenerator.generate_exchange(count)
        elif data_type == 'market':
            data = DataGenerator.generate_market_data(count, 3)
        else:
            raise ValueError(f"Unsupported data type: {data_type}")
        
        # Create API response structure
        response = {
            "status": {
                "timestamp": datetime.datetime.now().isoformat(),
                "error_code": 0,
                "error_message": None,
                "elapsed": random.randint(5, 100),
                "credit_count": 1
            },
            "data": data
        }
        
        return response
