import json
import requests
import re
import configSD


DEVICES_URL = "https://api.pushbullet.com/v2/devices"
CHATS_URL = "https://api.pushbullet.com/v2/chats"
CHANNELS_URL = "https://api.pushbullet.com/v2/channels-info"
ME_URL = "https://api.pushbullet.com/v2/users/me"
PUSH_URL = "https://api.pushbullet.com/v2/pushes"
UPLOAD_REQUEST_URL = "https://api.pushbullet.com/v2/upload-request"
EPHEMERALS_URL = "https://api.pushbullet.com/v2/ephemerals"


def sendToChannel(ID, Sale, Category):

    url = "https://www.slickdeals.net/f/"+str(ID)
    title = "[%s] %s" % (Category, Sale.decode('string_escape'))

    data_send = {"type": "link", "title": title, "body": "", "url": url,"channel_tag":  "creqdevtesting"}

    resp = requests.post('https://api.pushbullet.com/v2/pushes', data=json.dumps(data_send),
                         headers={'Authorization': 'Bearer ' + configSD.DEV_KEY, 'Content-Type': 'application/json'})

    if resp.status_code != 200:
        raise Exception("Push Failed")

def sendToSelf(ID, Sale, Category):

    url = "https://www.slickdeals.net/f/"+str(ID)
    title = "[%s] %s" % (Category, Sale)

    data_send = {"type": "link", "title": title, "body": "", "url": url}

    resp = requests.post('https://api.pushbullet.com/v2/pushes', data=json.dumps(data_send),
                         headers={'Authorization': 'Bearer ' + configSD.API_KEY, 'Content-Type': 'application/json'})

    if resp.status_code != 200:
        raise Exception("Push Failed")


