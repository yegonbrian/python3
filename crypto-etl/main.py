from api_client import CoinMarketCapClient
from etl_pipeline import CryptoETLPipeline
from visualization import CryptoVisualizer
from config import CMC_API_KEY
import sqlite3
import pandas as pd 

def query_sqlite_data(db_path='cryptocurrency_data.db'):
    """
    Query data from SQLite for visualization
    """
    conn = sqlite3.connect(db_path)
    query = """
    SELECT 
        id, name, symbol, price, market_cap, 
        percent_change_24h, volume_24h, 
        market_cap_category
    FROM cryptocurrencies
    """
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df

def main():
    # Initialize CoinMarketCap API Client
    client = CoinMarketCapClient(CMC_API_KEY)
    
    # Extract top 100 cryptocurrencies
    crypto_data = client.get_top_cryptocurrencies(limit=100)
    
    # Initialize ETL Pipeline
    etl_pipeline = CryptoETLPipeline(crypto_data)
    
    # Clean Data
    cleaned_data = etl_pipeline.clean_data()
    
    # Transform Data
    transformed_data = etl_pipeline.transform_data(cleaned_data)
    
    # Load Data to SQLite
    etl_pipeline.load_data(transformed_data)
    
    # Retrieve data from SQLite for visualization
    final_data = query_sqlite_data()
    
    # Visualize Data
    visualizer = CryptoVisualizer(final_data)
    
    # Create visualizations
    market_cap_plot = visualizer.create_market_cap_distribution()
    price_scatter_plot = visualizer.create_price_scatter()
    
    # Save plots
    visualizer.save_plots([market_cap_plot, price_scatter_plot])

if __name__ == "__main__":
    main()