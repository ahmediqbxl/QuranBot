import requests
import tweepy
import random
from datetime import datetime

# Authenticate to Twitter
auth = tweepy.OAuthHandler("consumer_key", "consumer_secret")
auth.set_access_token("access_token", "access_token_secret")

# Create API object
api = tweepy.API(auth)

# Page
page = 1

# Get a verse from the Quran API
url = "https://api.alquran.cloud/random/ayah"
url_english = f"http://api.alquran.cloud/v1/page/{page}/en.asad"
url_arabic = f"http://api.alquran.cloud/v1/page/{page}/quran-uthmani"
response = requests.get(url)
data = response.json()["data"][0]
text = data["text"]
surah = data["surah"]["name"]
number = data["numberInSurah"]

# Post the verse as a tweet
tweet = f"{text} ({surah} {number})"
api.update_status(tweet)

# Print a message to confirm the tweet was sent
now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
print(f"Tweet sent at {now}: {tweet}")
