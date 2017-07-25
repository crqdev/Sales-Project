from bs4 import BeautifulSoup
import requests
from PostData import *
import config


class SlickDeals:
    def __init__(self):
        self.posts = None


    def getSiteData(self):
        url = "https://slickdeals.net/forums/forumdisplay.php?f=9&order=desc&pp=150&sort=threadstarted"
        response = requests.get(url, timeout=15, allow_redirects=True)

        if response.status_code != 200:
            raise ConnectionError

        soup = BeautifulSoup(response.text, 'html.parser')
        head = soup.find("tbody", id="threadbits_forum_9")
        self.posts = head.findChildren('tr')


    def getNewPosts(self, timealivelimit):

        currentTime = int(time.time())
        posts = []

        for i in self.posts[1:]:
            post = PostData(i)
            post.extractID()
            post.extractCat()

            if post.category == "Moved":  # No point in tracking moved posts
                continue

            # Checking if sale is in a category we care about, otherwise go to next post
            try:
                Pass = config.Category_Screen[post.category]
            except:
                Pass = config.PASS_ALL_OTHER_CATEGORIES
            if not Pass:
                continue

            # Get info from post
            post.extractUTC()
            post.extractTitle()
            post.extractVR()
            post.extractVS()
            post.getTimeAlive(currentTime)


            # Adding Post to list of deals if it meets timelimit

            if post.timeAlive <= timealivelimit:
                temp = {
                    "source": "slickdeals",
                    "id": post.id,
                    "title": "[%s] %s" % (post.category, post.rawTitle),
                    "url": "https://slickdeals.net/f/%s" % post.id,
                    "views": post.views,
                    "created_utc": currentTime-post.timeAlive,
                    "timealive": post.timeAlive,
                    "score": post.score
                }
                posts.append(temp)
            else:
                break

        return posts

