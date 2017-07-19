import praw
import config
import time
import pymysql
import threading
import requests
import re
from pb_api import *

attemptpause = 5

def threadupdate(name, msg):
    print(name, " : ", msg)

def server_login():
    db = pymysql.connect(host=config.host, port=3306, user=config.s_user,
                              passwd=config.s_pass, db=config.db_name, charset='utf8mb4',
                                cursorclass=pymysql.cursors.DictCursor)
    cur = db.cursor()
    return db, cur


def bot_login():
    r = praw.Reddit(username=config.username,
					password=config.password,
					client_id=config.client_id,
					client_secret=config.client_secret,
					user_agent="TestingCRQdevBot v0.1")
    return r

def sendNotification(link, name):
    data = {}
    data["value1"] = name
    data["value2"] = link
    requests.post("https://maker.ifttt.com/trigger/buildapcsales/with/key/bFCLALt0S6UMac-T0D8qNk", data)

class newsubs (threading.Thread):
    #This just tracks new submissions being posted to the subreddit
    def __init__(self):
        threading.Thread.__init__(self)
        self.name = "newsub.thread"

    def run(self):

        data = """INSERT INTO Submissions(ID, Created, Title) VALUES ('%s', '%d', '%s')"""
        query = """SELECT MAX(Created) FROM Submissions"""

        while True:

            try:
                db, cur = server_login()
                r = bot_login()
                #cur.execute("SELECT VERSION()")
                #dataver = cur.fetchone()
                threadupdate(self.name, dataver)
                subreddit = r.subreddit('buildapcsales')
                cur.execute(query)
                results = cur.fetchone()
                aftertime = results['MAX(Created)']

                threadupdate(self.name, "Login Success")
                for i in subreddit.stream.submissions():
                    try:
                        if int(i.created_utc) > aftertime:
                            cur.execute(data % (str(i.shortlink), int(i.created_utc), re.escape(i.title)))
                            db.commit()
                            threadupdate(self.name, "Entry Added")
                    except:
                        db.rollback()
                        threadupdate(self.name, "Request Error")
                        raise
            except:
                threadupdate(self.name, "Login Failed")
                time.sleep(attemptpause)


class postdata (threading.Thread):
    # This collects post information from any post that less than 4 hours old and saves data to my mySQL server
    def __init__(self):
        threading.Thread.__init__(self)
        self.name = "postdata.thread"

    def run(self):
        while True:
            try:
                datat = """INSERT INTO PostData(upTime, sampleTime, ID, UPVOTES, COMMENTS, NSFW) VALUES ('%s', '%s', '%s', '%s', '%s', '%s')"""
                db, cur = server_login()
                r = bot_login()
                cur.execute("SELECT VERSION()")
                data = cur.fetchone()
                threadupdate(self.name, data)
                threadupdate(self.name, "Login Success")
                delay = 4 * 3600

                while True:
                    try:
                        count = 0
                        timefilter = int(time.time()) - delay
                        time1 = int(time.time())
                        startt = int(time.time())
                        subreddit = r.subreddit('buildapcsales')
                        for i in subreddit.stream.submissions():
                            count = count + 1
                            if (i.created_utc >= timefilter):
                                cur.execute(datat % (int(startt - i.created_utc), startt, str(i.shortlink), int(i.score), int(i.num_comments), str(i.over_18)))
                            if count >= 100:
                                break
                        db.commit()
                        threadupdate(self.name, "Data Collection Success")
                        time2 = int(time.time()) - time1
                        timesleep = 10 - time2
                        if timesleep < 10:
                            time.sleep(timesleep)
                        else:
                            continue
                    except:
                        threadupdate(self.name, "Request Failed")
                        time.sleep(10)
                        raise
            except:
                threadupdate(self.name, "Login Failed")
                time.sleep(attemptpause)



class notify (threading.Thread):
    #Constantly checks the data collected for posts that are between 0 and 300 seconds old. If they reach threschold, then notification is sent out.
    def __init__(self):
        threading.Thread.__init__(self)
        self.name = "notification.thread"

    def run(self):
        idealpost = """SELECT DISTINCT ID FROM PostData
                  WHERE upTime > '%d' AND upTime < '%d' AND  sampleTime > '%d' AND UPVOTES >= 3"""
        query = """SELECT * FROM Submissions WHERE ID = '%s'"""
        updateQ = """UPDATE Submissions SET Notify = 1 WHERE ID = '%s'"""
        while True:
            try:
                db, cur = server_login()
                cur.execute("SELECT VERSION()")
                data = cur.fetchone()
                threadupdate(self.name, data)
                threadupdate(self.name, "Login Success")

                while True:
                    startime = int(time.time())
                    try:
                        tfilter = int(time.time()) - 3600 * 1
                        cur.execute(idealpost % (0, 300, tfilter))
                        results = cur.fetchall()
                        for row in results:
                            cur.execute(query % row['ID'])
                            temp = cur.fetchone()
                            if temp['Notify'] == 0:
                                PushToSelf(temp['ID'], temp['Title'])
                                cur.execute(updateQ % temp['ID'])
                        db.commit()
                    except:
                        threadupdate(self.name, "Request Failed")
                        raise

                    processtime = int(time.time()) - startime
                    if processtime > 5:
                        continue
                    time.sleep((5 - processtime))

            except:
                threadupdate(self.name, "Login Failed")
                time.sleep(attemptpause)


newsubthread = newsubs()
newsubthread.start()
postdatathread = postdata()
postdatathread.start()
notifythread = notify()
notifythread.start()