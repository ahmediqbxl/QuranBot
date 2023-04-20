import tweepy
import json
import requests
from datetime import datetime

ACCESS_TOKEN = "1634000831333945345-ZH0vNkWDUPqx9SZiOp9soIOs7iSNfp"
ACCESS_TOKEN_SECRET = "4KEDaHbVr5H7BsRNw1O85504qyUoaTsg1pyWgcBJcq1kA"
BEARER_TOKEN = "AAAAAAAAAAAAAAAAAAAAAFhfmwEAAAAATyAphLi3SovuWwZzcsnbCXFLEbc%3D2hYsX3Dw9SifGD4AYEEoPsNK0rCCChvyouIgF6vFMglaP0CSyS"
API_KEY = "IadvsrqNGoG34IrLk1C989Egz"
API_KEY_SECRET = "NwiPh0h4CiLpAC9eVXiroHJPM0tEKqmMtHnUefZBgAk7rkNcqT"

# Set up the API endpoint
url_twitter = "https://api.twitter.com/2/tweets"

# Set up the authentication headers
headers = {
    "Authorization": f"Bearer {BEARER_TOKEN}",
    "User-Agent": "v2FilteredStreamPython"
}

# Authenticate to Twitter
auth = tweepy.OAuthHandler(
    API_KEY,
    API_KEY_SECRET
)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

# Create API object
api = tweepy.API(auth, wait_on_rate_limit=True)

# Page
page = 1

# Get a verse from the Quran API
url_english = f"http://api.alquran.cloud/v1/page/{page}/en.asad"
url_arabic = f"http://api.alquran.cloud/v1/page/{page}/quran-uthmani"
response = requests.get(url_english)

# print(response.content) # print the content of the response

json_data = json.loads(response.text)

text_list = [ayah['text'] for ayah in json_data['data']['ayahs']]
text = ' '.join(text_list)

surah = json_data['data']['ayahs'][0]['surah']['name']
surah_english = json_data['data']['ayahs'][0]['surah']['englishName']

number = json_data['data']['number']

print(text, ' Surah: ', surah, ' ', surah_english, ' Page Number: ', number) 

tweet_text = f"{text} ({surah} {number})"

# Set up the tweet parameters
params = {
    "text": tweet_text
}

# Send the tweet
response = requests.post(url_twitter, headers=headers, params=params)

# Print a message to confirm the tweet was sent
now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
print(f"Tweet sent at {now}: {tweet_text}")

