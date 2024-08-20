from alpha_vantage.timeseries import TimeSeries

# Define your API key
YOUR_API_KEY = 'ZCXL2CO1DH8YYJJX'

# Function to get the market price for a given symbol
def get_market_price(symbol):
    ts = TimeSeries(key=YOUR_API_KEY, output_format='pandas')
    data, meta_data = ts.get_intraday(symbol=symbol, interval='1min', outputsize='full')
    print("Data head:\n", data.head())  # Print the first few rows of the DataFrame
    print("Meta Data:\n", meta_data)    # Print metadata for verification
    return data['4. close'].iloc[0]  

# Get and print the market price for Apple Inc. (AAPL)
aapl_price = get_market_price('AAPL')
print(f"Apple Inc. (AAPL) price: {aapl_price}")
