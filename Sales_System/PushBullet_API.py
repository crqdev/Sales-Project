import json
import requests
import config


class PushBullet(object):
    @staticmethod
    def pushtoself(url, title):
        data_send = {"type": "link", "title": title, "body": "", "url": url}

        resp = requests.post('https://api.pushbullet.com/v2/pushes', data=json.dumps(data_send),
                             headers={'Authorization': 'Bearer ' + config.PushBullet_API_KEY,
                                      'Content-Type': 'application/json'})

        if resp.status_code != 200:
            raise ConnectionError

    @staticmethod
    def pushtochannel(url, title):
        data_send = {"type": "link", "title": title, "body": "", "url": url, "channel_tag": "crqdevdeals"}

        resp = requests.post('https://api.pushbullet.com/v2/pushes', data=json.dumps(data_send),
                             headers={'Authorization': 'Bearer ' + config.PushBullet_API_KEY,
                                      'Content-Type': 'application/json'})

        if resp.status_code != 200:
            raise ConnectionError

