import yfinance as yf


def get_stock_price(ticker_symbol):
    """
    Fetches the latest stock price for a given ticker symbol.
    """
    try:
        stock = yf.Ticker(ticker_symbol)
        stock_info = stock.history(period="1d")

        if not stock_info.empty:
            latest_price = stock_info['Close'].iloc[-1]  # Get the last closing price
            return round(latest_price, 2)
        else:
            return "Stock data not available."
    except Exception as e:
        return f"Error fetching stock data: {e}"


if __name__ == "__main__":
    ticker = input("Enter stock ticker symbol (e.g., AAPL, TSLA, GOOG): ")
    print(f"Latest {ticker} price: ${get_stock_price(ticker)}")
