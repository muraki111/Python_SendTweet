import json
import urllib.error
import urllib.request

# https://qiita.com/hiiii/items/caab4e41fc83b5b5c209


def send_line_notify(notification_message, imgURL):
    json_open = open('key.json', 'r')
    json_load = json.load(json_open)

    url = 'https://api.line.me/v2/bot/message/broadcast'
    channel_access_token = json_load['channel_access_token']
    data = {
        'messages': [{
            'type': 'text',
            'text': notification_message
        }]
    }
    jsonstr = json.dumps(data).encode('ascii')
    request = urllib.request.Request(url, data=jsonstr)
    request.add_header('Content-Type', 'application/json')
    request.add_header('Authorization', 'Bearer ' + channel_access_token)
    request.get_method = lambda: 'POST'
    response = urllib.request.urlopen(request)

    data = {
        'messages': [{
            "type": "image",
            "originalContentUrl": imgURL,
            "previewImageUrl": imgURL
        }]
    }
    jsonstr = json.dumps(data).encode('ascii')
    request = urllib.request.Request(url, data=jsonstr)
    request.add_header('Content-Type', 'application/json')
    request.add_header('Authorization', 'Bearer ' + channel_access_token)
    request.get_method = lambda: 'POST'
    response = urllib.request.urlopen(request)
