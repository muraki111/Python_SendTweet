from cgitb import text
import datetime
import random
import re
from sys import stdout
import time
from collections import Counter, defaultdict
from time import sleep

import demoji
import json
import tweepy
from janome.tokenizer import Tokenizer
from nltk import ngrams

import line_notify


# Twitter API設定
def twitter_api():
    CONSUMER_KEY = "KKEjabhXrWBowgZANEfFfsiOb"
    CONSUMER_SECRET = "IqKMOhcpVcA5g9oyPEDKXEomC5C0uAefNsE6HN1D9Iae4bMweD"
    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    ACCESS_TOKEN = "1404005926110068736-iiWLU09TuWENLDKDqEtigOhDei7jKk"
    ACCESS_SECRET = "xIPMqPdHzbYNYZK3FniIgaZxo71gRDO5KGvqNlt38Sx70"

    auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)

    return tweepy.API(auth)


# Tweet検索
def serch_word(api):
    # list = ""
    list = []

    results = api.user_timeline(screen_name="salmon_shift", count=1)
    for result in results:
        text = re.sub(r"https://t.co/[0-9a-zA-Z_]{1,15}", "", result.text)
        id = result.id

        imgURL = result.extended_entities['media'][0]['media_url_https']
    # print(str(results).replace(",", "\n"))
    return text, imgURL, id


if __name__ == '__main__':
    id_old, id_new = 0

    while True:
        try:
            dt_now = datetime.datetime.now()
            # Twitter API設定
            api = twitter_api()
            id_old = id_new
            notification_message, imgURL, id_new = serch_word(api)
            if id_old != id_new:
                line_notify.send_line_notify(notification_message, imgURL)

        except:
            pass
