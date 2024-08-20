import yfinance as yf
from datetime import date

# List of stock tickers
stocks = ['AAPL', 'GOOGL', 'AMZN', 'MSFT', 'TSLA', 'NVDA', 'META']
date = "2024-08-15"



def get_current_price(ticker):
        try:
            #print(f"Fetching price for ticker: {ticker}")  # Debugging line
            data = yf.download(ticker, period='1d', interval='1m')
            #print(f"Fetched data: {data}")  # Debugging line
            if not data.empty and 'Close' in data.columns:
                return data['Close'].iloc[-1]
            else:
                print(f"Data is empty or missing 'Close' column")  # Debugging line
            return 0.0
        except Exception as e:
            print(f"Error fetching price for {ticker}: {e}")  # Debugging line
            return 0.0

for ticker in stocks:
    
    stock = yf.Ticker(ticker)
   
    # Get stock information
    info = stock.info
    data = yf.download(ticker, period='5d',interval='1d')
    
    
    # Check if info is not None
    if info is not None:
        # Extract the required data
        price = get_current_price(ticker)
        market_cap = info.get('marketCap', 'N/A')
        volume = info.get('volume', 'N/A')
        pe_ratio = info.get('trailingPE', 'N/A')
        beta = info.get('beta', 'N/A')
        close_price = data['Close'][-2]
        change_percentage = ((price-close_price)/close_price)
    else:
        # Set default values
        price = 'N/A'
        market_cap = 'N/A'
        volume = 'N/A'
        pe_ratio = 'N/A'
        beta = 'N/A'

    # Print or process the data
    #print(f'Ticker: {ticker}')
    print(f'Price: ${price:,.2f}' if price != 'N/A' else 'Price: N/A')
    print(f'Market Cap: ${market_cap:,}' if market_cap != 'N/A' else 'Market Cap: N/A')
    print(f'Volume: {volume:,}' if volume != 'N/A' else 'Volume: N/A')
    print(f'P/E Ratio: {pe_ratio}' if pe_ratio != 'N/A' else 'P/E Ratio: N/A')
    print(f'Beta: {beta}' if beta != 'N/A' else 'Beta: N/A')
    print(f'Close Price: {close_price}' if close_price != 'N/A' else 'Close Price: N/A')
    print(f'Change Percentage: {change_percentage:.2%}' if change_percentage != 'N/A' else 'Change Percentage: N/A')

    print('---')






