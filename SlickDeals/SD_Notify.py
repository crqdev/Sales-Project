from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from ServerControl import *
from PostData import *
from PushBullet_API import *
import time
import sys

ua = UserAgent()
header = {'User-Agent': str(ua.chrome)}

def grabposts():
    url = "https://slickdeals.net/forums/forumdisplay.php?f=9&order=desc&pp=50&sort=threadstarted"
    htmlContent = requests.get(url, headers=header, timeout=15, allow_redirects=True)
    soup = BeautifulSoup(htmlContent.text, 'html.parser')
    head = soup.find("tbody", id="threadbits_forum_9")
    posts = head.findChildren('tr')
    return posts

while True:
    # try:
        server = ServerControl()
        server.connect()

        while True:
            startime = int(time.time())
            posts = grabposts()
            timestamp = (datetime.now() + timedelta(hours=4))

            for i in posts[1:]:
                post = PostData(i)
                post.extractID()
                post.extractCat()
                post.extractUTC()
                post.extractTimeAlive(startime)

                if post.category == "Moved":  # No point in tracking moved posts
                    continue

                if post.timeAlive > 700:
                    break
                post.extractVR()
                post.extractVS()
                post.extractTitle()

                if server.notificationStatus(post.id) == 0:
                    if post.timeAlive < 200 and post.views > 10:
                        sendToSelf(post.id, post.rawTitle, post.category)
                        server.setNotification(post.id)
                        server.commit()

                    elif post.timeAlive < 500 and post.views > 20:
                        sendToSelf(post.id, post.rawTitle, post.category)
                        server.setNotification(post.id)
                        server.commit()

                    elif post.timeAlive < 900 and post.views > 100:
                        sendToSelf(post.id, post.rawTitle, post.category)
                        server.setNotification(post.id)
                        server.commit()
                else:
                    continue

            totaltime = (time.time()) - startime
            print("Process took ", totaltime)
            sleeptime = 10-totaltime
            if sleeptime <= 0:
                print("Not Sleeping, took over 10 seconds")
                continue
            else:
                print("Sleeping for ", sleeptime, "\n")
                time.sleep(sleeptime)
z
    # except:
    #     print("Unexpected error:", sys.exc_info()[0])
    #     time.sleep(30)

