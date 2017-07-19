import requests
import json
import config

def PushToSelf(URL, Title):

    data_send = {"type": "link", "title": Title, "body": "", "url": URL}

    resp = requests.post('https://api.pushbullet.com/v2/pushes', data=json.dumps(data_send),
                         headers={'Authorization': 'Bearer ' + config.API_KEY, 'Content-Type': 'application/json'})

    if resp.status_code != 200:
        raise Exception("Push Failed")


