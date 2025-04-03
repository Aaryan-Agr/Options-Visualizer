import yfinance as yf
import plotly.graph_objects as go

class OptionTracker:
    def __init__(self, ticker):
        self.ticker = ticker    # Stock Ticker
        self.regions = []       # Stores all profit/loss regions

    def get_stock_price(self):
        """Fetch the live stock price from Yahoo Finance."""
        try:
            ticker_data = yf.Ticker(self.ticker)
            todays_data = ticker_data.history(period='1d')
            return todays_data['Close'].iloc[0]
        except Exception as e:
            return f"Error fetching price: {e}"

    def execute_option(self, strike_price, premium, ct, cta):
        """
        Executes an option and determines the profit region automatically.
        
        Parameters:
        - strike_price (float): The option strike price
        - premium (float): The contract premium paid/received
        - ct (str): 'Call' or 'Put'
        - cta (str): 'Buy' or 'Sell'
        """

        min_price, max_price = None, None

        if ct == "Call":
            if cta == "Buy":
                min_price = strike_price  # Profit above strike price
            else:  # Sell Call
                max_price = strike_price + premium  # Profit if price stays below this

        elif ct == "Put":
            if cta == "Buy":
                max_price = strike_price  # Profit below strike price
            else:  # Sell Put
                min_price = strike_price - premium  # Profit if price stays above this

        # Store the new acceptance region
        new_region = (min_price if min_price is not None else float('-inf'),
                      max_price if max_price is not None else float('inf'))
        self.regions.append({
            'type': ct,
            'action': cta,
            'strike_price': strike_price,
            'premium': premium,
            'region': new_region
        })

        print(f"Option executed: {ct} {cta} at ${strike_price}, Premium: ${premium}")
        print(f"Updated Acceptance Regions: {self.regions}")

tracker = OptionTracker("AAPL")
tracker.execute_option(strike_price=210, premium=5, ct="Call", cta="Buy")
tracker.execute_option(strike_price=260, premium=6, ct="Put", cta="Buy")
tracker.execute_option(strike_price=270, premium=7, ct="Call", cta="Sell")



