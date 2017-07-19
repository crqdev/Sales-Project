import pymysql
import configSD
import time
from datetime import datetime, date, timedelta, timezone
class ServerControl():

    def __init__(self):
        self.db = None
        self.cur = None
        self.tracked = None

    def connect(self):
        db = pymysql.connect(host=configSD.host, port=configSD.port, user=configSD.user,
                             passwd=configSD.passwd, db=configSD.dbname, charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)
        cur = db.cursor()
        self.db = db
        self.cur = cur

    def close(self):
        self.db.close()

    def isNewPost(self, ID):
        if self.tracked == ():
            return True

        if int(ID) > int(self.tracked[0]['ID']):
            return True
        return False

    def inTimeframe(self, TimeAlive):
        if TimeAlive >= 4*3600:
            return False
        return True

    def addPost(self, ID, Title, TS, Cat):
        queryPost = """INSERT INTO Posts(ID, Title, Creation, Category) VALUES ('%s', '%s', '%s', '%s')"""
        self.cur.execute(queryPost % (ID, Title, TS, Cat))

    def commit(self):
        self.db.commit()

    def addData(self, ID, Timestamp, TA, Votes, Score, Views, Replies, CAT):
        queryData = """INSERT INTO PostData(ID, Timestamp, TimeAlive, Votes, Score, Views, Replies, Category) VALUES ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')"""
        self.cur.execute(queryData % (ID, Timestamp, TA, Votes, Score, Views, Replies, CAT))

    def addManyPosts(self,Data):
        queryData = """INSERT INTO PostData(ID, Timestamp, TimeAlive, Votes, Score, Views, Replies, Category) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"""
        self.cur.executemany(queryData, Data)

    def getTrackedPosts(self, seconds=3600*4):
        timestamp = datetime.now() + timedelta(hours=4)
        delay = (timestamp - timedelta(seconds=seconds)).strftime("%Y-%m-%d %H:%M:%S")
        query = """SELECT ID FROM Posts WHERE Creation > '%s' ORDER BY ID DESC"""
        self.cur.execute(query % delay)
        self.tracked = self.cur.fetchall()


    def notificationStatus(self, ID):
        query = """SELECT Notify from Posts WHERE ID = %s"""
        self.cur.execute(query % ID)
        result = self.cur.fetchone()
        if result == None:
            return 1
        return result['Notify']

    def setNotification(self, ID):
        updateQ = """UPDATE Posts SET Notify = 1 WHERE ID = '%s'"""
        self.cur.execute(updateQ % ID)
