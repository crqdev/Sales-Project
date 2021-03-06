import re
from datetime import datetime, date, timedelta, timezone
import time

class PostData():
    """
    Class that has built in methods that extract information from each threadpost in slickdeals forum

    """

    def __init__(self, data):
        self.data = data
        self.id = None
        self.title = None
        self.votes = None
        self.score = None
        self.views = None
        self.replies = None
        self.timestamp = None
        self.category = None
        self.timeAlive = None
        self.rawTitle = None

    def extractUTC(self):
        # Extract Time UTC
        tempdatetime = self.data.find(id="td_postdate_" + self.id).find("div").contents
        creationdate = tempdatetime[0].strip()
        creationtime = tempdatetime[1].contents[0].strip()
        creationtime = datetime.strptime(creationtime, '%I:%M %p').strftime("%H:%M")
        if creationtime >= "21:00" and creationtime <= "23:59":
            if creationdate == "Today":
                creationdate = (date.today()).strftime("%m-%d-%y")
            elif creationdate == "Yesterday":
                creationdate = (date.today() - timedelta(2)).strftime("%m-%d-%y")
        else:
            if creationdate == "Today":
                creationdate = (date.today()).strftime("%m-%d-%y")
            elif creationdate == "Yesterday":
                creationdate = (date.today() - timedelta(1)).strftime("%m-%d-%y")
        timestamp = datetime.strptime(creationdate + " " + creationtime, "%m-%d-%y %H:%M")
        self.timestamp = timestamp + timedelta(hours=7)

    def extractVS(self):
        # Getting Votes and Score
        viewcount = self.data.find(id="td_threadtitle_" + self.id).find("img", {"class": "concat-thumbs"})
        if viewcount != None:
            viewcount = viewcount["alt"]
            votes = re.findall("Votes: (\d+)", viewcount)[0]
            score = re.findall("Score: ([+-]?\d+)", viewcount)[0]
        else:
            votes = 0
            score = 0
        self.votes = votes
        self.score = score

    def extractVR(self):
        # Getting Views and Replies
        viewrep = self.data.find("td", {"title": re.compile("Replies: ")})["title"]
        viewrep = viewrep.replace(',', '')
        views = re.findall("Views: (\d+)", viewrep)[0]
        replies = re.findall("Replies: (\d+)", viewrep)[0]
        self.views = int(views)
        self.replies = int(replies)

    def extractTitle(self):
        # Getting Title using constant part of ID and post ID
        title = self.data.find(id="thread_title_" + self.id).contents[0]
        self.title = re.escape(title)
        self.rawTitle = title

    def extractID(self):
        # Finding Post ID using Regex
        ID = self.data.find("td", id=re.compile("td_threadstatusicon_"))["id"].split("_")[2]
        self.id = ID

    def extractCat(self):
        try:
            category = self.data.find("td", {"class": "tlv3_cat"}).find("a").contents[0]
        except:
            category = "Moved"
        self.category = category

    def extractTimeAlive(self, current):
        self.timeAlive = int(current - time.mktime(self.timestamp.timetuple()) + 4*3600)
        if self.timeAlive < 0:
            print("ERROR")

    def getDetails(self):
        self.extractTitle()
        self.extractUTC()

    def getStats(self):
        self.extractVR()
        self.extractVS()






