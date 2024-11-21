import sqlite3
import pandas as pd
from datetime import datetime

class DatabaseManager:
    def __init__(self, db_path='cryptocurrency_data.db'):
        """
        Initialize database connection
        """
        self.db_path = db_path
        self.conn = None
        self.cursor = None
    
    def connect(self):
        """
        Establish a connection to the SQLite database
        """
        try:
            self.conn = sqlite3.connect(self.db_path)
            self.cursor = self.conn.cursor()
            print(f"Connected to database: {self.db_path}")
        except sqlite3.Error as error:
            print(f"Error connecting to the database: {error}")
            raise
    
    def create_tables(self):
        """
        Create tables for cryptocurrency data
        """
        try:
            # Create main cryptocurrency table
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS cryptocurrencies (
                    id INTEGER PRIMARY KEY,
                    name TEXT,
                    symbol TEXT,
                    price REAL,
                    market_cap REAL,
                    percent_change_24h REAL,
                    volume_24h REAL,
                    market_cap_category TEXT,
                    extraction_timestamp DATETIME
                )
            ''')
            
            # Create historical tracking table
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS price_history (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    crypto_id INTEGER,
                    price REAL,
                    timestamp DATETIME,
                    FOREIGN KEY (crypto_id) REFERENCES cryptocurrencies(id)
                )
            ''')
            
            self.conn.commit()
            print("Tables created successfully")
        except sqlite3.Error as error:
            print(f"Error creating tables: {error}")
            raise
    
    def insert_cryptocurrency_data(self, data):
        """
        Insert cryptocurrency data into SQLite database
        """
        try:
            # Convert DataFrame to list of tuples for bulk insertion
            data_to_insert = data[[
                'id', 'name', 'symbol', 'price', 'market_cap', 
                'percent_change_24h', 'volume_24h', 
                'market_cap_category', 'extraction_timestamp'
            ]].values.tolist()
            
            # Insert data into cryptocurrencies table
            self.cursor.executemany('''
                INSERT OR REPLACE INTO cryptocurrencies (
                    id, name, symbol, price, market_cap, 
                    percent_change_24h, volume_24h, 
                    market_cap_category, extraction_timestamp
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', data_to_insert)
            
            self.conn.commit()
            print(f"Inserted {len(data_to_insert)} cryptocurrency records")
        except sqlite3.Error as error:
            print(f"Error inserting cryptocurrency data: {error}")
            self.conn.rollback()
            raise
    
    def insert_price_history(self, data):
        """
        Insert price history for tracking
        """
        try:
            # Create price history entries
            price_history = []
            current_time = datetime.now()
            
            for _, row in data.iterrows():
                price_history.append((
                    row['id'],  # crypto_id
                    row['price'],  # price
                    current_time  # timestamp
                ))
            
            self.cursor.executemany('''
                INSERT INTO price_history (
                    crypto_id, price, timestamp
                ) VALUES (?, ?, ?)
            ''', price_history)
            
            self.conn.commit()
            print(f"Inserted {len(price_history)} price history records")
        except sqlite3.Error as error:
            print(f"Error inserting price history: {error}")
            self.conn.rollback()
            raise
    
    def close(self):
        """
        Close database connection
        """
        if self.conn:
            self.conn.close()
            print("Database connection closed")