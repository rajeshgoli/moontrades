import openai

def extract_trade_details(tweet_text):
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": """You are a trading assistant that extracts structured trade details from tweets. 
            
            **Instructions:**
            - Read the tweet and determine if it contains an actionable trade signal.
            - If it's a trade entry, extract the **ticker symbol, option type (CALL/PUT), strike price, expiration date, and entry price**.
            - If it's a profit update, extract **percentage gain, sell level, or runner strategy**.
            - If it's an exit signal, extract **exit reason (stop-loss, breakeven, profit-taking, etc.)**.
            - If it's general commentary, ignore it.
            - Always return JSON output in the following format:
            
            ```json
            {
                "action": "Trade Entry | Profit Update | Trade Exit | Ignore",
                "ticker": "M",
                "option_type": "CALL",
                "strike_price": 15,
                "expiration_date": "2025-02-14",
                "entry_price": 0.11,
                "profit_target": 500
            }
            ```
            
            - If a field is not present in the tweet, return `null` for that field.
            - Do not return any extra text outside of the JSON object.
            """},
            {"role": "user", "content": f"Analyze this tweet and extract structured trade details:\n\n{tweet_text}"}
        ]
    )
    
    return response["choices"][0]["message"]["content"]

# Example usage
tweet = "$M 15 CALL 2/14 @ .11 500% POTENTIAL"
trade_details = extract_trade_details(tweet)
print(trade_details)
