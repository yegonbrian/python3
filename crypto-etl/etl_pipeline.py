import pandas as pd
from datetime import datetime
import os
from db import DatabaseManager

class CryptoETLPipeline:
    def __init__(self, data):
        self.data = data
        self.db_manager = DatabaseManager()
    
    def clean_data(self):
        """
        Clean and preprocess cryptocurrency data
        """
        # Remove any rows with missing data
        cleaned_data = self.data.dropna()
        
        # Convert price and market cap to numeric
        cleaned_data['price'] = pd.to_numeric(cleaned_data['price'], errors='coerce')
        cleaned_data['market_cap'] = pd.to_numeric(cleaned_data['market_cap'], errors='coerce')
        
        return cleaned_data
    
    def transform_data(self, cleaned_data):
        """
        Add derived columns and perform transformations
        """
        transformed_data = cleaned_data.copy()
        
        # Add extraction timestamp as a string
        transformed_data['extraction_timestamp'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        # Categorize cryptocurrencies by market cap
        transformed_data['market_cap_category'] = pd.cut(
            transformed_data['market_cap'], 
            bins=[0, 1e9, 10e9, 100e9, float('inf')],
            labels=['Small', 'Medium', 'Large', 'Mega']
        )
        
        return transformed_data
    
    def load_data(self, transformed_data):
        """
        Load processed data into SQLite database
        """
        # Establish database connection
        self.db_manager.connect()
        
        # Create necessary tables
        self.db_manager.create_tables()
        
        # Insert cryptocurrency data
        self.db_manager.insert_cryptocurrency_data(transformed_data)
        
        # Insert price history
        self.db_manager.insert_price_history(transformed_data)
        
        # Close database connection
        self.db_manager.close()
        
        return transformed_data