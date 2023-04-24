import os
import tweepy
import json
import requests
from datetime import datetime

def setup_credentials():
    with open('secrets.json', 'r') as json_file:
        data = json.load(json_file)

    ACCESS_TOKEN = data.get('ACCESS_TOKEN')
    ACCESS_TOKEN_SECRET = data.get('ACCESS_TOKEN_SECRET')
    BEARER_TOKEN = data.get('BEARER_TOKEN')
    API_KEY = data.get('API_KEY')
    API_KEY_SECRET = data.get('API_KEY_SECRET')
    CLIENT_ID = data.get('CLIENT_ID')
    CLIENT_SECRET = data.get('CLIENT_SECRET')

    auth = tweepy.OAuthHandler(
        API_KEY, API_KEY_SECRET
        )
    auth.set_access_token(
            ACCESS_TOKEN, ACCESS_TOKEN_SECRET
            )
    api = tweepy.API(auth)

    return api

def load_page():
    # Load the current page number from a file or database
    if os.path.isfile('page.txt'):
        with open('page.txt', 'r') as page_file:
            page = int(page_file.read().strip())
    else:
        page = 1

    return page

def retrieve_text(page):
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

    return tweet_text

def split_tweet(tweet_text):
    """
    Splits tweet into multiple tweets of 280 characters or less, maintaining word integrity.
    Returns a list of tweet texts.
    """
    tweet_parts = []
    while len(tweet_text) > 0:
        if len(tweet_text) <= 280:
            tweet_parts.append(tweet_text)
            break
        split_index = tweet_text[:280].rfind(' ')
        if split_index == -1:
            split_index = 279
        tweet_parts.append(tweet_text[:split_index])
        tweet_text = tweet_text[split_index+1:]
    return tweet_parts

def send_tweet_thread(api, tweet_parts, in_reply_to_status_id=None):
    """
    Posts a thread of tweets. First tweet is posted as a new tweet, and all subsequent tweets are posted
    as replies to the previous tweet in the thread.
    """
    last_tweet_id = None
    for i, tweet_text in enumerate(tweet_parts):
        try:
            if i == 0:
                # post the first tweet as a new tweet
                status = api.update_status(status=tweet_text)
            else:
                # post subsequent tweets as replies to the previous tweet
                status = api.update_status(status=tweet_text, in_reply_to_status_id=last_tweet_id)
            print("Tweet successfully posted!")
            last_tweet_id = status.id_str
        except Exception as e:
            print("Error posting tweet:", e)
            return
    

def send_tweets(api, tweet_text, page):
    # Check if the tweet text is longer than 280 characters (the current Twitter character limit)
    if len(tweet_text) > 280:

        # Split the tweet text into multiple tweets
        tweet_parts = split_tweet(tweet_text)

        # Post the tweet thread
        send_tweet_thread(api, tweet_parts)

    else:

        # If the tweet text is less than or equal to 280 characters, just post a single tweet
        api.update_status(tweet_text)

    # Increment the page number and save it to a file or database
    page += 1
    with open('page.txt', 'w') as page_file:
        page_file.write(str(page))

def execute():
    api = setup_credentials()
    page = load_page()
    text = retrieve_text(page)

    send_tweets(api, text, page)

if __name__ == "__main__":
    execute()