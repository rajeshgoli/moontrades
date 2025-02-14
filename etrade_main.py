import requests
import json
import openai
import time

# E*TRADE API Credentials
ETRADE_CONSUMER_KEY = "YOUR_CONSUMER_KEY"
ETRADE_CONSUMER_SECRET = "YOUR_CONSUMER_SECRET"
ETRADE_ACCESS_TOKEN = "YOUR_ACCESS_TOKEN"
ETRADE_ACCESS_SECRET = "YOUR_ACCESS_SECRET"
ETRADE_ACCOUNT_ID = "YOUR_ACCOUNT_ID"

# API Base URL (Use Sandbox for Paper Trading)
BASE_URL = "https://apisb.etrade.com"


def place_trade(trade_data):
    """Executes a trade using the E*TRADE API with a 10% slippage buffer."""
    order_url = f"{BASE_URL}/v1/accounts/{ETRADE_ACCOUNT_ID}/orders/place.json"
    headers = {
        "Authorization": f"Bearer {ETRADE_ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }

    # Adjusting for slippage: Allow entry price to be 10% higher
    adjusted_entry_price = round(trade_data["entry_price"] * 1.10, 2)

    order_payload = {
        "orderType": "LIMIT",
        "priceType": "LIMIT",
        "limitPrice": adjusted_entry_price,
        "quantity": 1,  # Adjust based on risk
        "orderTerm": "GTC",
        "symbol": trade_data["ticker"],
        "orderAction": "BUY_TO_OPEN",
        "orderStrategyType": "SINGLE",
        "securityType": "OPTN",
        "optionType": trade_data["option_type"],
        "strikePrice": trade_data["strike_price"],
        "expirationDate": trade_data["expiration_date"]
    }

    response = requests.post(order_url, json=order_payload, headers=headers)
    
    if response.status_code == 200:
        print(f"✅ Trade Executed: {trade_data['ticker']} {trade_data['strike_price']} {trade_data['option_type']} @ {adjusted_entry_price} (adjusted for slippage)")
    else:
        print(f"❌ Trade Execution Failed: {response.json()}")

def place_sell_order(trade_data):
    """Places a limit sell order for profit-taking at the target percentage (e.g., 500%)."""
    if trade_data["profit_target"]:
        sell_price = trade_data["entry_price"] * (trade_data["profit_target"] / 100)
        sell_payload = {
            "orderType": "LIMIT",
            "priceType": "LIMIT",
            "limitPrice": round(sell_price, 2),
            "quantity": 1,
            "orderTerm": "GTC",
            "symbol": trade_data["ticker"],
            "orderAction": "SELL_TO_CLOSE",
            "securityType": "OPTN"
        }
        order_url = f"{BASE_URL}/v1/accounts/{ETRADE_ACCOUNT_ID}/orders/place.json"
        headers = {"Authorization": f"Bearer {ETRADE_ACCESS_TOKEN}", "Content-Type": "application/json"}
        
        response = requests.post(order_url, json=sell_payload, headers=headers)
        if response.status_code == 200:
            print(f"✅ Profit Target Set: Selling {trade_data['ticker']} at {round(sell_price, 2)}")
        else:
            print(f"❌ Sell Order Failed: {response.json()}")

def process_tweet(tweet_text):
    """Processes a tweet: Extracts intent, then executes trade or action accordingly."""
    trade_data = extract_trade_details(tweet_text)
    
    if trade_data["action"] == "Trade Entry":
        print(f"🚀 New Trade Signal: {trade_data}")
        place_trade(trade_data)
        if trade_data["profit_target"]:
            place_sell_order(trade_data)

    elif trade_data["action"] == "Profit Update":
        print(f"💰 Profit Update Detected: {trade_data}")

    elif trade_data["action"] == "Trade Exit":
        print(f"🛑 Exit Signal: {trade_data}")

    else:
        print(f"🔍 No Action Needed: {tweet_text}")

