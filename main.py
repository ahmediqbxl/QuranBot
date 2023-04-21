import tweepy
import json
import requests
from datetime import datetime

with open('secrets.json', 'r') as json_file:
    data = json.load(json_file)

ACCESS_TOKEN = data.get('ACCESS_TOKEN')
ACCESS_TOKEN_SECRET = data.get('ACCESS_TOKEN_SECRET')
BEARER_TOKEN = data.get('BEARER_TOKEN')
API_KEY = data.get('API_KEY')
API_KEY_SECRET = data.get('API_KEY_SECRET')
CLIENT_ID = data.get('CLIENT_ID')
CLIENT_SECRET = data.get('CLIENT_SECRET')

username = 'Quran4Soul'
page = 1

# Get a verse from the Quran API
url_english = f"http://api.alquran.cloud/v1/page/{page}/en.asad"
url_arabic = f"http://api.alquran.cloud/v1/page/{page}/quran-uthmani"
response = requests.get(url_english)

json_data = json.loads(response.text)

text_list = [ayah['text'] for ayah in json_data['data']['ayahs']]
text = ' '.join(text_list)

surah = json_data['data']['ayahs'][0]['surah']['name']
surah_english = json_data['data']['ayahs'][0]['surah']['englishName']

number = json_data['data']['number']

print(text, ' ', surah, surah_english, ' Page: ', number) 

tweet_text = f"{text} ({surah}, {surah_english}, Page {number})"

auth = tweepy.OAuthHandler(
        API_KEY, API_KEY_SECRET
        )
auth.set_access_token(
        ACCESS_TOKEN, ACCESS_TOKEN_SECRET
        )
api = tweepy.API(auth)

def send_tweet(tweet_body, in_reply_to_status_id=None):
    try:
        status = api.update_status(status=tweet_body, in_reply_to_status_id=in_reply_to_status_id)
        print("Tweet successfully posted!")
    except Exception as e:
        print("Error posting tweet:", e)

    return status 


# Check if the tweet text is longer than 280 characters (the current Twitter character limit)
if len(tweet_text) > 280:

    # Split the tweet text into two parts
    tweet_part1 = tweet_text[:280]
    tweet_part2 = tweet_text[280:] 

    # Post the first tweet
    tweet1 = api.update_status(tweet_part1)

    # Post the second tweet as a reply to the first one
    tweet2 = api.update_status(tweet_part2, in_reply_to_status_id=tweet1.id_str)

else:

    # If the tweet text is less than or equal to 280 characters, just post a single tweet
    api.update_status(tweet_text)



