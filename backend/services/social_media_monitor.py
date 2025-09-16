# services/twitter_monitor.py
import os
import tweepy
import requests
from dotenv import load_dotenv

load_dotenv()

# Your FastAPI backend URL
API_URL = "http://localhost:8000/api/hazards/report"
BEARER_TOKEN = os.getenv("TWITTER_BEARER_TOKEN")

# Keywords to track. #ADD MORE
HAZARD_KEYWORDS = [
    "#chennaifloods", "#chennairains", "power cut", 
    "roadblock", "tree fall", "water logging"
]

class HazardStream(tweepy.StreamingClient):
    def on_tweet(self, tweet):
        print(f"Potential hazard detected: {tweet.text}")
        
        # Basic filter to avoid retweets or irrelevant posts
        if tweet.text.startswith("RT @"):
            return

        # TODO: A more advanced version would extract location from the tweet
        # For now, we'll use a default location for Chennai
        payload = {
            'title': f"Social Media Alert: {tweet.text[:50]}...",
            'description': tweet.text,
            'hazard_type': 'social_media_alert', # A new category
            'latitude': 13.0827, # Chennai latitude
            'longitude': 80.2707, # Chennai longitude
            'report_source': 'twitter'
        }
        
        try:
            # Send the data to your own API
            # Note: The API expects multipart/form-data, so we send it as 'data'
            response = requests.post(API_URL, data=payload)
            if response.status_code == 201:
                print("Successfully submitted report to Synapse API.")
            else:
                print(f"Failed to submit report. Status: {response.status_code}, Body: {response.text}")
        except Exception as e:
            print(f"Error connecting to API: {e}")

# Setup and run the stream
stream = HazardStream(BEARER_TOKEN)

# Clear existing rules (optional, good for testing)
if stream.get_rules().data:
    rule_ids = [rule.id for rule in stream.get_rules().data]
    stream.delete_rules(rule_ids)

# Add new rules to the stream
for keyword in HAZARD_KEYWORDS:
    stream.add_rules(tweepy.StreamRule(keyword))

print("Starting Twitter stream...")
stream.filter()