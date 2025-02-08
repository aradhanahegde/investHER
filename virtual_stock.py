Better spam filters … Now Drive automatically moves suspicious files shared with you to spam. You can still report spam on your own.Learn more
from stock_api import get_stock_price


class VirtualStockMarket:
    def __init__(self, initial_balance=10000):
        self.balance = initial_balance  # Virtual currency
        self.portfolio = {}  # Holds purchased stocks

    def buy_stock(self, ticker, quantity):
        price = get_stock_price(ticker)
        if isinstance(price, str):  # Check if there's an error
            print(price)
            return

        total_cost = price * quantity
        if total_cost > self.balance:
            print("Not enough funds to complete this purchase.")
        else:
            self.balance -= total_cost
            if ticker in self.portfolio:
                self.portfolio[ticker]['quantity'] += quantity
                self.portfolio[ticker]['total_spent'] += total_cost
            else:
                self.portfolio[ticker] = {'quantity': quantity, 'total_spent': total_cost}
            print(f"Bought {quantity} shares of {ticker} at ${price} each. Remaining balance: ${self.balance:.2f}")

    def sell_stock(self, ticker, quantity):
        if ticker not in self.portfolio or self.portfolio[ticker]['quantity'] < quantity:
            print("You don't own enough shares to sell.")
            return

        price = get_stock_price(ticker)
        if isinstance(price, str):
            print(price)
            return

        total_earnings = price * quantity
        self.balance += total_earnings
        self.portfolio[ticker]['quantity'] -= quantity
        if self.portfolio[ticker]['quantity'] == 0:
            del self.portfolio[ticker]  # Remove stock if all shares are sold

        print(f"Sold {quantity} shares of {ticker} at ${price} each. New balance: ${self.balance:.2f}")

    def view_portfolio(self):
        print("\nYour Portfolio:")
        if not self.portfolio:
            print("You don't own any stocks yet.")
        else:
            for ticker, data in self.portfolio.items():
                avg_price = data['total_spent'] / data['quantity']
                print(f"{ticker}: {data['quantity']} shares (Avg. Price: ${avg_price:.2f})")
        print(f"Available Balance: ${self.balance:.2f}\n")


if __name__ == "__main__":
    market = VirtualStockMarket()

    while True:
        action = input("Enter action (buy, sell, view, exit): ").strip().lower()

        if action == "buy":
            ticker = input("Enter stock ticker symbol: ").upper()
            quantity = int(input("Enter quantity: "))
            market.buy_stock(ticker, quantity)

        elif action == "sell":
            ticker = input("Enter stock ticker symbol: ").upper()
            quantity = int(input("Enter quantity: "))
            market.sell_stock(ticker, quantity)

        elif action == "view":
            market.view_portfolio()

        elif action == "exit":
            print("Exiting virtual stock market.")
            break

        else:
            print("Invalid action. Please enter 'buy', 'sell', 'view', or 'exit'.")
