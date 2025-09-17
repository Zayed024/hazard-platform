# services/social_media_monitor.py
import os
import tweepy
import requests
import json
import time
import random
from dotenv import load_dotenv

# --- Configuration ---
load_dotenv()

# Set to True to read from 'mock_tweets.json' instead of the live Twitter API
DEMO_MODE = True

# Your FastAPI backend URL
API_URL = "http://localhost:8000/api/hazards/report"
BEARER_TOKEN = os.getenv("TWITTER_BEARER_TOKEN")

# Keywords to track when DEMO_MODE is False
HAZARD_KEYWORDS = [
    "#chennaifloods", "#chennairains", "power cut", 
    "roadblock", "tree fall", "water logging", "cyclone alert"
]

# --- Core Logic ---

def process_tweet_text(tweet_text, is_demo=False):
    """
    Processes a tweet's text, determines its source, and sends it to the Synapse API.
    """
    source = 'twitter_simulation' if is_demo else 'twitter'
    print(f"Processing potential hazard from {source}: {tweet_text}")
    
    # Basic filter to avoid retweets
    if tweet_text.startswith("RT @"):
        print("Skipping retweet.")
        return

    # Prepare the payload for our API
    payload = {
        'title': f"Social Media Alert: {tweet_text[:45]}...",
        'description': tweet_text,
        'hazard_type': 'social_media_alert',
        'latitude': 13.0827 + random.uniform(-0.05, 0.05), # Randomize location around Chennai
        'longitude': 80.2707 + random.uniform(-0.05, 0.05),
        'report_source': source
    }
    
    try:
        # Send the data to your own API as form data
        response = requests.post(API_URL, data=payload)
        
        if response.status_code == [201,200]:
            print(f"✅ Successfully submitted report from {source} to Synapse API.")
        else:
            print(f"❌ Failed to submit report. Status: {response.status_code}, Body: {response.text}")
    except Exception as e:
        print(f"❌ Error connecting to API: {e}")

# --- Main Execution Block ---

if __name__ == "__main__":
    if DEMO_MODE:
        print("🚀 Starting Twitter stream in DEMO MODE...")
        print("   Reading from mock_tweets.json every 10 seconds.")
        
        try:
            with open('mock_tweets.json', 'r') as f:
                mock_tweets = json.load(f)
            
            while True:
                tweet = random.choice(mock_tweets)
                process_tweet_text(tweet['text'], is_demo=True)
                time.sleep(10) # Wait for 10 seconds before posting the next one
        except FileNotFoundError:
            print("❌ ERROR: 'services/mock_tweets.json' not found. Cannot run in DEMO_MODE.")
        except KeyboardInterrupt:
            print("\n⏹️  Demo mode stopped by user.")

    else:
        print("🚀 Starting LIVE Twitter stream...")
        
        if not BEARER_TOKEN:
            print("❌ ERROR: TWITTER_BEARER_TOKEN not found in .env file. Cannot run in live mode.")
        else:
            # This is the class for handling the live Twitter stream
            class HazardStream(tweepy.StreamingClient):
                def on_tweet(self, tweet):
                    process_tweet_text(tweet.text, is_demo=False)

                def on_error(self, status_code):
                    print(f"❌ Live stream error: {status_code}")
                    return False # Return False to stop the stream on critical errors

            # Setup and run the stream
            stream = HazardStream(BEARER_TOKEN)
            
            try:
                # Clear any existing rules before adding new ones
                if stream.get_rules().data:
                    rule_ids = [rule.id for rule in stream.get_rules().data]
                    print(f"   Clearing {len(rule_ids)} existing rule(s)...")
                    stream.delete_rules(rule_ids)

                # Add new rules from our keyword list
                print(f"   Adding {len(HAZARD_KEYWORDS)} new rule(s)...")
                for keyword in HAZARD_KEYWORDS:
                    stream.add_rules(tweepy.StreamRule(keyword))

                print("   ✅ Live stream connected and filtering for keywords...")
                stream.filter()

            except KeyboardInterrupt:
                print("\n⏹️  Live stream stopped by user.")
            except Exception as e:
                print(f"💥 An unexpected error occurred with the live stream: {e}")