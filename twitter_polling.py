import requests
import time

# Twitter API Credentials
BEARER_TOKEN = "YOUR_TWITTER_BEARER_TOKEN"
USER_ID = "REPLACE_WITH_USER_ID"

LAST_TWEET_ID = None

def get_latest_tweets():
    """Fetch the last 5 tweets"""
    url = f"https://api.twitter.com/2/users/{USER_ID}/tweets?max_results=5"
    headers = {"Authorization": f"Bearer {BEARER_TOKEN}"}

    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json().get("data", [])
    return []

while True:
    tweets = get_latest_tweets()
    if tweets:
        for tweet in tweets:
            tweet_id = tweet["id"]
            tweet_text = tweet["text"]
            
            if tweet_id != LAST_TWEET_ID:  # Only process new tweets
                print(f"New Tweet: {tweet_text}")
                LAST_TWEET_ID = tweet_id
                process_tweet(tweet_text)  # Execute trade logic

    # Adaptive polling
    current_hour = time.localtime().tm_hour
    if 9 <= current_hour < 11 or 15 <= current_hour < 16:
        time.sleep(60)  # Fast polling during peak trading hours
    elif 11 <= current_hour < 15:
        time.sleep(120)  # Slower polling midday
    else:
        time.sleep(300)  # Very slow polling after market close
