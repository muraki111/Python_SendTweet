import datetime
import re
import time

import tweepy

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
    imgURL = []
    videoURL = []
    videoFlag = 0

    results = api.user_timeline(screen_name="AGE_Tsumugi", count=1, tweet_mode='extended')
    for result in results:
        text = re.sub(r"https://t.co/[0-9a-zA-Z_]{1,15}", "", result.full_text)
        try:
            videoURL.append(result.extended_entities['media'][0]['video_info']['variants'][0]['url'])
            videoFlag = 1
        except:
            pass
        try:
            for i in range(4):
                imgURL.append(result.extended_entities['media'][i]['media_url_https'])
        except:
            pass
    # .extended_entities["media"][0]["media_url_https"]
    # print(str(results).replace(",", "\n"))
    return text, imgURL, videoURL, id, videoFlag


if __name__ == '__main__':
    id_new = 0
    id_old = 0

    dt_now = datetime.datetime.now()
    try:
        # Twitter API設定
        api = twitter_api()
        id_old = id_new
        notification_message, imgURL, videoURL, id_new, videoFlag = serch_word(api)
        if id_old != id_new:
            line_notify.send_line_text(notification_message)
            if videoFlag:
                line_notify.send_line_video(imgURL[0], videoURL[0])
            else:
                for i in range(len(imgURL)):
                    line_notify.send_line_img(imgURL[i])
        else:
            time.sleep(600)
    except:
        pass
