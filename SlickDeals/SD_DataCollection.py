from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import requests
import time
from ServerControl import *
from PostData import *

import sys


ua = UserAgent()
header = {'User-Agent': str(ua.chrome)}


def grabposts():
    url = "https://slickdeals.net/forums/forumdisplay.php?f=9&order=desc&pp=150&sort=threadstarted"
    htmlContent = requests.get(url, headers=header, timeout=15, allow_redirects=True)
    soup = BeautifulSoup(htmlContent.text, 'html.parser')
    head = soup.find("tbody", id="threadbits_forum_9")
    posts = head.findChildren('tr')
    return posts

while True:
    try:
        server = ServerControl()
        server.connect()

        while True:
            startime = int(time.time())
            print(startime)
            posts = grabposts()
            timestamp = (datetime.now() + timedelta(hours=4))
            server.getTrackedPosts(3600*4)
            ValidPostData = []

            for i in posts[1:]:
                post = PostData(i)
                post.extractID()
                post.extractCat()
                if post.category == "Moved":  # No point in tracking moved posts
                    continue

                post.extractUTC()
                post.extractVR()
                post.extractVS()
                post.extractTimeAlive(startime)
                post.extractTitle()

                if server.isNewPost(post.id):  # Add Post to Tracking Table
                    server.addPost(post.id, post.title, post.timestamp, post.category)
                    # server.addData(post.id, timestamp.strftime("%Y-%m-%d %H:%M:%S"), post.timeAlive, post.votes, post.score, post.views, post.replies, post.category)
                    ValidPostData.append([post.id, timestamp.strftime("%Y-%m-%d %H:%M:%S"), post.timeAlive, post.votes, post.score, post.views, post.replies, post.category])

                    continue

                if server.inTimeframe(post.timeAlive): #Add Post Data if within time range(LEss than hours old)
                    # server.addData(post.id, timestamp.strftime("%Y-%m-%d %H:%M:%S"), post.timeAlive, post.votes,
                    #                post.score, post.views, post.replies, post.category)
                    ValidPostData.append(
                        [post.id, timestamp.strftime("%Y-%m-%d %H:%M:%S"), post.timeAlive, post.votes, post.score,
                         post.views, post.replies, post.category])
                else:
                    break
            print(ValidPostData)
            server.addManyPosts(ValidPostData)
            server.commit()
            ValidPostData = []
            totaltime = int(time.time()) - startime
            print("Process took ", totaltime)
            sleeptime = 10-totaltime
            if sleeptime <= 0:
                print("Not Sleeping, took over 10 seconds")
                continue
            else:
                print("Sleeping for ", sleeptime, "\n")
                time.sleep(sleeptime)

    except:
        print("Unexpected error:", sys.exc_info()[0])
        time.sleep(20)

