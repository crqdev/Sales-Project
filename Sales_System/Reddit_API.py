import requests
import config
import time


class Reddit:

    def __init__(self):
        self.connection = None
        self.useragent = "SalesBot by %s" % config.reddit_username
        self.token = None

    def login(self, ):
        client_auth = requests.auth.HTTPBasicAuth(config.reddit_client_id, config.reddit_client_secret)
        post_data = {"grant_type": "password", "duration": "permanent", "username": config.reddit_username, "password": config.reddit_password}

        headers = {"User-Agent": self.useragent}
        response = requests.post("https://www.reddit.com/api/v1/access_token", auth=client_auth, data=post_data,
                                 headers=headers)
        if response.status_code == 200:
            self.token = response.json()["access_token"]
        else:
            raise ConnectionError

    def getNewPosts(self, subreddit, agelimit):
        currentTime = int(time.time())
        url = "https://oauth.reddit.com/r/%s/new" % subreddit
        post_data = {"limit": "100"}
        headers = {"Authorization": "bearer " + self.token, "User-Agent": self.useragent}
        response = requests.get(url, headers=headers,  data=post_data)

        if response.status_code == 200:
            data = response.json()['data']["children"]
        elif response.status_code == 401:  # Token has expired, get new token, try request again
            self.login()
            headers = {"Authorization": "bearer " + self.token, "User-Agent": self.useragent}
            response = requests.get(url, headers=headers, data=post_data)
            data = response.json()['data']["children"]
        else:
            raise ConnectionError

        posts = []

        for i in data:
            if currentTime - i["data"]['created_utc'] <= agelimit:
                temp = {"source": "reddit",
                        "id": i["data"]["id"],
                        "title": i["data"]["title"],
                        "url": "https://redd.it/" + i["data"]["id"],
                        "score": i["data"]["score"],
                        "created_utc": i["data"]['created_utc'],
                        "timealive": currentTime - i["data"]['created_utc']}

                posts.append(temp)
            else:
                break

        return posts
