import plotly.express as px 
import plotly.graph_objs as go 

class CryptoVisualizer:
    def __init__(self, data):
        self.data = data

    def create_market_cap_distribution(self):
        '''
        Create a pie chart showing market cap distribution
        '''
        market_cap_summary = self.data.groupby('market_cap_category')['market_cap'].sum()

        fig = px.pie(
            values=market_cap_summary.values, 
            names=market_cap_summary.index,
            title="Cryptocurrency Market Cap Distribution", 
            hole=0.3
        )

        return fig 
    
    def create_price_scatter(self):
        '''
        Create a scatter plot of cryptocurrencies prices 
        '''
        fig = px.scatter(
            self.data, 
            x='market_cap', 
            y='price',
            color='market_cap_category', 
            size='market_cap',
            hover_name='name', 
            title='Cryptocurrency Price v Market Cap', 
            labels={'market_cap': 'Market Cap (USD)', 'price': 'Price (USD)'}
        )
        return fig 
    
    def save_plots(self, plots, output_dir='Visualizations')
        '''
        Save Plotly figures as HTML files 
        '''
        import os 
        os.makedirs(output_dir, exist_ok=True)

        for i, fig in enumerate(plots, 1):
            fig.write_html(f"{output_dir}/crypto_plot_{i}.html")