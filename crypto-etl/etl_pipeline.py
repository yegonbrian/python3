import pandas as pd 
from datetime import datetime 
import os 
from db import DatabaseManager

class CryptoETLPipeline: 
    def __init__(self, data):
        self.data = data
        self.db_manager = DatabaseManager()

    def clean_data(self): 
        '''
        Clean & preprocess crypto data and returned a cleaned pandas dataframe
        '''
        cleaned_data = self.data.dropna() # Remove any rows with missing data
        # Convert price and market cap to numeric
        cleaned_data['price'] = pd.to_numeric(cleaned_data['price'], errors='coerce')
        cleaned_data['market_cap'] = pd.to_numeric(cleaned_data['market_cap'], errors='coerce')

        return cleaned_data
    
    def transform_data(self, cleaned_data):
        '''
        Add derived columns and perform transformations
        Args: cleaned_data (pandas.DataFrame): cleaned crypto data
        Returns pandas.DataFrame: transformed data
        '''
        transformed_data = cleaned_data.copy()
        transformed_data['extraction_timestamp'] = datetime.now() # Add extraction timestamp

        # Categorize crypto by marketcap 
        transformed_data['market_cap_category'] = pd.cut(
            transformed_data['market_cap'], 
            bins=[0, 1e9, 10e9, 100e9, float('inf')],
            labels=['Small','Medium','Large','Mega']
        )

        return transformed_data
    
    def load_data(self, transformed_data, output_dir='data'):
        '''
        Save processed data into CSV, Parquet Formats and Into Databases i.e SQLite3, PostgreSQL, MongoDB
        Args: 
            transformed_data (pandas.DataFrame): Transformed cryptocurrency data
            output_dir (str): Directory to save output files
        '''
        os.makedirs(output_dir, exist_ok=True) # Create output directory if it doesn't exist
        timestamp = datetime.now().strftime("%Y%m%dc_%H%M%S") # Generate filename with timestamp

        # Save to CSV 
        csv_path = os.path.join(output_dir, f'Crypto_data_{timestamp}.csv')
        transformed_data.to_csv(csv_path, index=False)

        # Save to Parquet (more efficient for big data)
        parquet_path = os.path.join(output_dir, f'Crypto_data{timestamp}.parquet')
        transformed_data.to_parquet(parquet_path, index=False)

        # Save to SQLite3
        self.db_manager.connect() # Establish Database Connection
        self.db_manager.create_tables() # Create necessary tables
        self.db_manager.insert_cryptocurrency_data(transformed_data) # Insert cryptocurrency data
        self.db_manager.insert_price_history(transformed_data) # Insert price history
        self.db_manager.close() # Close database connection

        print(f"Data Saved to {csv_path} and {parquet_path}")

        return transformed_data