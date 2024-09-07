import requests
import json
from prettytable import PrettyTable

# Replace with your Alpha Vantage API key
API_KEY = 'ac6d4fcdf40c4778b2dc1d4a95f27a20'

# File to store the portfolio
portfolio_file = 'portfolio.json'

# Load or initialize portfolio
def load_portfolio():
    try:
        with open(portfolio_file, 'r') as f:
            portfolio = json.load(f)
    except FileNotFoundError:
        portfolio = {}
    return portfolio

# Save portfolio
def save_portfolio(portfolio):
    with open(portfolio_file, 'w') as f:
        json.dump(portfolio, f)

# Add stock to portfolio
def add_stock(portfolio, symbol, shares):
    portfolio[symbol] = portfolio.get(symbol, 0) + shares
    save_portfolio(portfolio)

# Remove stock from portfolio
def remove_stock(portfolio, symbol):
    if symbol in portfolio:
        del portfolio[symbol]
        save_portfolio(portfolio)
    else:
        print(f"Stock {symbol} not found in portfolio.")

# Fetch stock price
def fetch_stock_price(symbol):
    url = f"https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol={symbol}&interval=1min&apikey={API_KEY}"
    response = requests.get(url)
    data = response.json()
    try:
        last_refreshed = data["Meta Data"]["3. Last Refreshed"]
        last_price = data["Time Series (1min)"][last_refreshed]["4. close"]
        return float(last_price)
    except KeyError:
        print(f"Failed to retrieve data for {symbol}.")
        return None

# Display portfolio
def display_portfolio(portfolio):
    table = PrettyTable()
    table.field_names = ["Stock Symbol", "Shares", "Current Price", "Total Value"]

    total_value = 0.0
    for symbol, shares in portfolio.items():
        price = fetch_stock_price(symbol)
        if price:
            value = price * shares
            total_value += value
            table.add_row([symbol, shares, f"${price:.2f}", f"${value:.2f}"])

    print(table)
    print(f"Total Portfolio Value: ${total_value:.2f}")

# Main program loop
def main():
    portfolio = load_portfolio()

    while True:
        print("\nStock Portfolio Tracker")
        print("1. Add Stock")
        print("2. Remove Stock")
        print("3. View Portfolio")
        print("4. Exit")
        choice = input("Choose an option: ")

        if choice == '1':
            symbol = input("Enter stock symbol: ").upper()
            shares = int(input("Enter number of shares: "))
            add_stock(portfolio, symbol, shares)
        elif choice == '2':
            symbol = input("Enter stock symbol to remove: ").upper()
            remove_stock(portfolio, symbol)
        elif choice == '3':
            display_portfolio(portfolio)
        elif choice == '4':
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
