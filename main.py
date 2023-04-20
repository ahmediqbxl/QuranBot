import tweepy
import requests
import random
from datetime import datetime

ACCESS_TOKEN = "1634000831333945345-ZH0vNkWDUPqx9SZiOp9soIOs7iSNfp"
ACCESS_TOKEN_SECRET = "4KEDaHbVr5H7BsRNw1O85504qyUoaTsg1pyWgcBJcq1kA"
BEARER_ROKEN = "AAAAAAAAAAAAAAAAAAAAAFhfmwEAAAAATyAphLi3SovuWwZzcsnbCXFLEbc%3D2hYsX3Dw9SifGD4AYEEoPsNK0rCCChvyouIgF6vFMglaP0CSyS"
API_KEY = "IadvsrqNGoG34IrLk1C989Egz"
API_KEY_SECRET = "NwiPh0h4CiLpAC9eVXiroHJPM0tEKqmMtHnUefZBgAk7rkNcqT"

# Authenticate to Twitter
auth = tweepy.OAuth1UserHandler(
    API_KEY,
    API_KEY_SECRET,
    ACCESS_TOKEN,
    ACCESS_TOKEN_SECRET
)

# Create API object
api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

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

