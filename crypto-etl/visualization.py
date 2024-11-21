import plotly.express as px
import plotly.graph_objs as go
import pandas as pd
import sqlite3

class CryptoVisualizer:
    def __init__(self, db_path='cryptocurrency_data.db'):
        """
        Initialize visualizer with database connection
        """
        self.conn = sqlite3.connect(db_path)
    
    def get_crypto_data(self):
        """
        Retrieve cryptocurrency data from database
        """
        query = """
        SELECT name, symbol, price, market_cap, percent_change_24h, market_cap_category
        FROM cryptocurrencies
        ORDER BY market_cap DESC
        """
        return pd.read_sql_query(query, self.conn)
    
    def market_cap_distribution(self):
        """
        Create market cap distribution pie chart
        """
        df = self.get_crypto_data()
        market_cap_summary = df.groupby('market_cap_category')['market_cap'].sum()
        
        return px.pie(
            values=market_cap_summary.values, 
            names=market_cap_summary.index,
            title='Cryptocurrency Market Cap Distribution',
            hole=0.3
        )
    
    def price_vs_market_cap_scatter(self):
        """
        Create scatter plot of price vs market cap
        """
        df = self.get_crypto_data()
        
        return px.scatter(
            df, 
            x='market_cap', 
            y='price', 
            color='market_cap_category',
            size='market_cap',
            hover_name='name',
            title='Cryptocurrency Price vs Market Cap',
            labels={'market_cap': 'Market Cap (USD)', 'price': 'Price (USD)'}
        )
    
    def price_change_bar_chart(self):
        """
        Create bar chart of 24h price changes
        """
        df = self.get_crypto_data()
        top_gainers = df.nlargest(10, 'percent_change_24h')
        top_losers = df.nsmallest(10, 'percent_change_24h')
        
        # Combine top gainers and losers
        comparison_df = pd.concat([top_gainers, top_losers])
        
        return px.bar(
            comparison_df, 
            x='name', 
            y='percent_change_24h',
            color='percent_change_24h',
            title='Top Cryptocurrency Price Changes (24h)',
            labels={'percent_change_24h': '24h Change (%)', 'name': 'Cryptocurrency'}
        )
    
    def save_plots(self, plots, output_dir='visualizations'):
        """
        Save Plotly figures as HTML files
        """
        import os
        os.makedirs(output_dir, exist_ok=True)
        
        for i, fig in enumerate(plots, 1):
            fig.write_html(f'{output_dir}/crypto_plot_{i}.html')
    
    def close(self):
        """Close database connection"""
        self.conn.close()

def main():
    visualizer = CryptoVisualizer()
    
    # Generate plots
    market_cap_plot = visualizer.market_cap_distribution()
    price_scatter_plot = visualizer.price_vs_market_cap_scatter()
    price_change_plot = visualizer.price_change_bar_chart()
    
    # Save plots
    visualizer.save_plots([
        market_cap_plot, 
        price_scatter_plot, 
        price_change_plot
    ])
    
    # Close database connection
    visualizer.close()

if __name__ == "__main__":
    main()