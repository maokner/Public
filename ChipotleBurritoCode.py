import os
import time
from pynput.keyboard import Key, Controller
import snscrape.modules.twitter as sntwitter
import datetime
import re
import requests
import pytesseract
from PIL import Image
os.system("open -a Messages")

keyboard = Controller()
def getrecentTweets(user):
    scraper = sntwitter.TwitterUserScraper(user)
    tweet_data = []
    for tweet in scraper.get_items():
        tweet_data.append([tweet.date, tweet.rawContent])
        break
    if tweet_data:
        time_now = datetime.datetime.now()
        if tweet_data[0][0].minute == time_now.minute:
            if not tweet.media:
                text = tweet_data[0][1]
                text = re.sub(r"\n|\s", "", text)
                return text
            else:

                for medium in tweet.media:
                    if isinstance(medium, sntwitter.Photo):
                        r = requests.get(medium.fullUrl)

                        with open('twitter_image.jpg', 'wb') as fp:
                            fp.write(r.content)
                        img = Image.open('twitter_image.jpg')
                        text = pytesseract.image_to_string(img, lang="eng")
                        text = re.sub(r"\n|\s", "", text)

                        return text
        else:
            return None



def extract_string(text):
    text = text.lower()
    pattern = r"text(\S+)to888222"
    match = re.search(pattern, text)
    if match:
        return match.group(1)
    else:
        return None

def send_message(message):

    keyboard.type(message.upper())
    time.sleep(1)
    keyboard.press(Key.enter)

while True:

    account = "ChipotleTweets"
    tweet_text = getrecentTweets(account)
    if tweet_text is not None:
         code = extract_string(tweet_text)
         if code != None:
             print(code)
             send_message(code)
             break



         else:
             print(tweet_text)
             print("No code found")
             continue


    else:
        continue


