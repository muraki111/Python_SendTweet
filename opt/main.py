import os
import re
import time
from datetime import datetime
from pathlib import Path

import joblib
import toml
import tweepy
from dateutil.relativedelta import relativedelta

import line_notify


# Twitter API設定
def twitter_api():
    toml_open = open('settings.toml', 'r')
    toml_load = toml.load(toml_open)

    CONSUMER_KEY = toml_load['Twitter']['CONSUMER_KEY']
    CONSUMER_SECRET = toml_load['Twitter']['CONSUMER_SECRET']
    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)

    ACCESS_TOKEN = toml_load['Twitter']['ACCESS_TOKEN']
    ACCESS_SECRET = toml_load['Twitter']['ACCESS_SECRET']
    auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)

    return tweepy.API(auth, wait_on_rate_limit=True)


# Tweet検索
def serch_word(api, UserID, TweetID):
    mediaURL = []
    results = api.user_timeline(screen_name=UserID, count=5, tweet_mode='extended')
    message = None

    for result in reversed(results):
        if str(result.full_text[:2]) != 'RT' and str(result.full_text[:1]) != '@':
            mediaURL = []

            # Tweet文章
            message = result.full_text

            # Tweetが text, photo, video か判別する
            try:
                Tweettype = result.extended_entities['media'][0]['type']

                # 写真、動画のURL削除
                message = re.sub(r' https://t.co/[0-9a-zA-Z_]{1,15}', '', result.full_text)
            except:
                Tweettype = 'text'

            if Tweettype == 'text':
                mediaURL.append('text')

            elif Tweettype == 'photo':
                mediaURL.append('photo')
                try:
                    for i in range(4):
                        mediaURL.append(result.extended_entities['media'][i]['media_url_https'])
                except:
                    pass

            elif Tweettype == 'video':
                mediaURL.append('video')
                mediaURL.append(result.extended_entities['media'][0]['media_url_https'])
                mediaURL.append(result.extended_entities['media'][0]['video_info']['variants'][0]['url'])

            # メッセージの末尾にTweetURLを追記
            message += '\n\nhttps://twitter.com/'+str(UserID)+'/status/'+str(result.id)

            # ユーザー名とプロフィール写真のURLを格納
            mediaURL.append(result.user.screen_name)
            mediaURL.append(result.user.name[:20].split(" ")[0])
            mediaURL.append(result.user.profile_image_url_https)

            TweetID = result.id

    return TweetID, message, mediaURL


def TweetID_fileCheck():
    for i in range(len(toml_load['Twitter']['UserID'])):
        TweetID_path = Path('./opt/TweetID/TweetID_' + toml_load['Twitter']['UserID'][i])
        if not os.path.isfile(TweetID_path):
            TweetID_path.touch(exist_ok=True)
            joblib.dump(None, TweetID_path, compress=3)


if __name__ == '__main__':
    # TwetterAPI設定
    api = twitter_api()

    toml_open = open('settings.toml', 'r')
    toml_load = toml.load(toml_open)
    TweetID_fileCheck()

    # -----------loop
    while (True):
        try:
            for i in range(len(toml_load['Twitter']['UserID'])):
                # UserID取得
                UserID = toml_load['Twitter']['UserID'][i]

                # 最後に送信したTweetID取得
                TweetID = joblib.load('./opt/TweetID/TweetID_' + UserID)
                TweetID_old = TweetID

                # Tweet取得
                TweetID, message, mediaURL = serch_word(api, UserID, TweetID)

                # # 最後に送信したTweetIDが古かった場合
                if TweetID != TweetID_old:
                    # LINEで送信
                    line_notify.send_data(message, mediaURL)

                    # TweetIDの更新
                    joblib.dump(TweetID, './opt/TweetID/TweetID_'+toml_load['Twitter']['UserID'][i], compress=3)
        except:
            dt1 = datetime.now()
            dt2 = dt1 + relativedelta(months=1, day=1, hour=0, minute=0, second=0, microsecond=0)

            print(UserID, 'Error : ', dt1)
            time.sleep((dt2-dt1).total_seconds())

        time.sleep(60)
