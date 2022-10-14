import json
import urllib.error
import urllib.request

import toml

# 固定 mediaURL[0]: type
# 可変 mediaURL[1]: img
# 可変 mediaURL[2]: img or video
# 可変 mediaURL[3]: img
# 可変 mediaURL[4]: img
# 固定 mediaURL[6]: UserID
# 固定 mediaURL[7]: UserName
# 固定 mediaURL[8]: ProfileImgURL


def create_data(message, mediaURL):
    toml_open = open('settings.toml', 'r')
    toml_load = toml.load(toml_open)

    data = {"messages": [{"type": "text", "text": message}]}
    icon = {"sender": {"name": mediaURL[len(mediaURL)-2], "iconUrl": mediaURL[len(mediaURL)-1]}}

    if toml_load['Twitter']['UserID'][0] != mediaURL[len(mediaURL)-3]:
        data["messages"][0].update(icon)

    if mediaURL[0] == 'photo':
        for i in range(len(mediaURL)-4):
            data_photo = {"type": "image", "originalContentUrl": mediaURL[i+1], "previewImageUrl": mediaURL[i+1]}
            data["messages"].append(data_photo)

            if toml_load['Twitter']['UserID'][0] != mediaURL[len(mediaURL)-3]:
                data["messages"][i+1].update(icon)

    elif mediaURL[0] == 'video':
        data_video = {"type": "video", "originalContentUrl": mediaURL[2], "previewImageUrl": mediaURL[1], "trackingId": "track-id"}
        data["messages"].append(data_video)

        if toml_load['Twitter']['UserID'][0] != mediaURL[len(mediaURL)-3]:
            data["messages"][1].update(icon)

    return data


def send_data(message, mediaURL):
    if(mediaURL != []):
        data = create_data(message, mediaURL)

        toml_open = open('settings.toml', 'r')
        toml_load = toml.load(toml_open)
        apiURL = toml_load['LINE']['apiURL']
        channel_access_token = toml_load['LINE']['channel_access_token']

        jsonstr = json.dumps(data).encode('ascii')
        request = urllib.request.Request(apiURL, data=jsonstr)
        request.add_header('Content-Type', 'application/json')
        request.add_header('Authorization', 'Bearer ' + channel_access_token)
        request.get_method = lambda: 'POST'
        response = urllib.request.urlopen(request)
