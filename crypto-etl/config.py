import os 
from dotenv import load_dotenv

load_dotenv()

CMC_API_KEY = os.getenv('CMC_API_KEY')
BASE_URL = 'https://pro-api.coinmarketcap.com/v1'