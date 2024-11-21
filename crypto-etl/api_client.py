import requests
import pandas as pd
from config import CMC_API_KEY, BASE_URL

class CoinMarketCapClient:
    def __init__(self, api_key):
        self.headers = {
            'Accepts': 'application/json',
            'X-CMC_PRO_API_KEY': api_key,
        }
        # Create a new session and update headers
        self.session = requests.Session()
        self.session.headers.update(self.headers)

    def get_top_cryptocurrencies(self, limit=100):
        """
        Fetch top cryptocurrencies by market cap
        """
        url = f'{BASE_URL}/cryptocurrency/listings/latest'
        parameters = {
            'start': '1',
            'limit': str(limit),
            'convert': 'USD'
        }
        
        try:
            response = self.session.get(url, params=parameters)
            data = response.json()
            
            # Extract relevant information
            crypto_data = []
            for coin in data['data']:
                crypto_data.append({
                    'id': coin['id'],
                    'name': coin['name'],
                    'symbol': coin['symbol'],
                    'price': coin['quote']['USD']['price'],
                    'market_cap': coin['quote']['USD']['market_cap'],
                    'percent_change_24h': coin['quote']['USD']['percent_change_24h'],
                    'volume_24h': coin['quote']['USD']['volume_24h']
                })
            
            return pd.DataFrame(crypto_data)
        
        except requests.exceptions.RequestException as e:
            print(f"Error fetching cryptocurrency data: {e}")
            return pd.DataFrame()