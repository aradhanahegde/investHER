from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.spinner import Spinner
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from stock_data import get_stock_price, buy_stock, sell_stock, portfolio, STOCK_TICKERS


class StockUI(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(orientation="vertical", **kwargs)

        # Portfolio Balance
        self.balance_label = Label(text=f"Balance: ${portfolio['balance']}", font_size=20)
        self.add_widget(self.balance_label)

        # Stock Selection Dropdown
        self.stock_spinner = Spinner(
            text="Select a stock",
            values=list(STOCK_TICKERS.keys()),  # Dropdown options
            size_hint=(1, 0.1)
        )
        self.add_widget(self.stock_spinner)

        self.search_button = Button(text="Get Stock Price", size_hint=(1, 0.1))
        self.search_button.bind(on_press=self.show_stock_price)
        self.add_widget(self.search_button)

        self.stock_price_label = Label(text="Stock Price: $0.00", font_size=18)
        self.add_widget(self.stock_price_label)

        # Buy/Sell Section
        self.quantity_input = TextInput(hint_text="Enter quantity", size_hint=(1, 0.1), input_filter="int")
        self.add_widget(self.quantity_input)

        self.buy_button = Button(text="Buy Stock", size_hint=(1, 0.1))
        self.buy_button.bind(on_press=self.buy_stock)
        self.add_widget(self.buy_button)

        self.sell_button = Button(text="Sell Stock", size_hint=(1, 0.1))
        self.sell_button.bind(on_press=self.sell_stock)
        self.add_widget(self.sell_button)

        # Portfolio Section
        self.portfolio_label = Label(text=self.get_portfolio_text(), font_size=18)
        self.add_widget(self.portfolio_label)

    def show_stock_price(self, instance):
        company = self.stock_spinner.text
        if company == "Select a stock":
            self.show_popup("Error", "Please select a company.")
            return

        price = get_stock_price(company)
        if isinstance(price, float):
            self.stock_price_label.text = f"Stock Price: ${price:.2f}"
        else:
            self.show_popup("Error", price)

    def buy_stock(self, instance):
        company = self.stock_spinner.text
        if company == "Select a stock":
            self.show_popup("Error", "Please select a company.")
            return

        quantity = self.quantity_input.text
        if not quantity.isdigit():
            self.show_popup("Error", "Please enter a valid quantity.")
            return

        message = buy_stock(company, int(quantity))
        self.show_popup("Transaction Result", message)
        self.update_ui()

    def sell_stock(self, instance):
        company = self.stock_spinner.text
        if company == "Select a stock":
            self.show_popup("Error", "Please select a company.")
            return

        quantity = self.quantity_input.text
        if not quantity.isdigit():
            self.show_popup("Error", "Please enter a valid quantity.")
            return

        message = sell_stock(company, int(quantity))
        self.show_popup("Transaction Result", message)
        self.update_ui()

    def update_ui(self):
        self.balance_label.text = f"Balance: ${portfolio['balance']}"
        self.portfolio_label.text = self.get_portfolio_text()

    def get_portfolio_text(self):
        holdings = "\n".join([f"{ticker}: {qty} shares" for ticker, qty in portfolio["stocks"].items()])
        return f"Portfolio:\n{holdings}" if holdings else "Portfolio: No stocks yet"

    def show_popup(self, title, message):
        popup = Popup(title=title, content=Label(text=message), size_hint=(0.6, 0.4))
        popup.open()


class StockApp(App):
    def build(self):
        return StockUI()


if __name__ == "__main__":
    StockApp().run()
