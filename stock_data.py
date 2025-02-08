import requests

portfolio = {
    "balance": 10000,  # Starting virtual balance
    "stocks": {}  # Stores bought stocks
}

# Dictionary of stock tickers for dropdown
STOCK_TICKERS = {
    "Apple": "AAPL",
    "Microsoft": "MSFT",
    "Tesla": "TSLA",
    "Amazon": "AMZN",
    "Google": "GOOGL",
    "Nvidia": "NVDA",
    "Meta": "META"
}


def get_stock_price(company):
    if company not in STOCK_TICKERS:
        return "Invalid company. Choose from the dropdown."

    ticker = STOCK_TICKERS[company]
    url = f"https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={ticker}&apikey=demo"

    try:
        response = requests.get(url).json()
        price = float(response["Global Quote"]["05. price"])
        return price
    except (KeyError, IndexError, ValueError):
        return "Stock price unavailable. Try again later."


def buy_stock(company, quantity):
    if company not in STOCK_TICKERS:
        return "Invalid company selection."

    price = get_stock_price(company)
    if isinstance(price, str):
        return price  # Return error message

    total_cost = price * quantity
    if portfolio["balance"] >= total_cost:
        portfolio["balance"] -= total_cost
        ticker = STOCK_TICKERS[company]
        portfolio["stocks"][ticker] = portfolio["stocks"].get(ticker, 0) + quantity
        return f"Bought {quantity} shares of {company} ({ticker}) for ${total_cost:.2f}."
    else:
        return "Insufficient balance."


def sell_stock(company, quantity):
    if company not in STOCK_TICKERS:
        return "Invalid company selection."

    ticker = STOCK_TICKERS[company]
    if ticker in portfolio["stocks"] and portfolio["stocks"][ticker] >= quantity:
        price = get_stock_price(company)
        total_value = price * quantity
        portfolio["balance"] += total_value
        portfolio["stocks"][ticker] -= quantity
        if portfolio["stocks"][ticker] == 0:
            del portfolio["stocks"][ticker]  # Remove empty stocks
        return f"Sold {quantity} shares of {company} ({ticker}) for ${total_value:.2f}."
    else:
        return "Not enough shares to sell."
