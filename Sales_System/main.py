from Reddit_API import *
from NotificationLog import *
from PushBullet_API import *
from SlickDeals import *
from NotificationHandler import *
import config



reddit = Reddit()
reddit.login()

SD = SlickDeals()

while True:

        timenow = time.time()
        # Get Posts From Reddit
        reddit_posts = reddit.getNewPosts('buildapcsales', config.reddit_agelimit)

        # Get Posts from SlickDeals
        SD.getSiteData()
        SD_posts = SD.getNewPosts(config.SD_agelimit)

        # Check if Notification Threshold Met In Either
        reddit_posts = reddit_threshold(reddit_posts)
        SD_posts = SD_threshold(SD_posts)

        # Read Notification Log to Ensure no double notification
        Log = NotificationLog.read()
        New_Posts = []

        print("********************************")

        # Compare Old Posts to Currents ones
        for i in reddit_posts:
            Match = False
            if Log == []:
                New_Posts.append(i)
                continue
            for j in Log:
                if str(i["id"]) == str(j["id"]):
                    Match = True
                    break
            if not Match:
                New_Posts.append(i)

        for i in SD_posts:
            Match = False
            if Log == []:
                New_Posts.append(i)
                continue
            for j in Log:
                if str(i["id"]) == str(j["id"]):
                    Match = True
                    break
            if not Match:
                New_Posts.append(i)

        # Send Notification and Append Log
        for i in New_Posts:
            Log.append(i)
            print("Sending Out:", i)
            PushBullet.pushtochannel(i["url"], i["title"])

        # Write New Log
        NotificationLog.update_log(Log, int(timenow))

        # Sleep For Ten Seconds
        processtime = time.time() - timenow
        print("Processing Took: ", processtime, "Seconds")
        if processtime > 10:
            print("Processing took over 10 seconds, not sleeping")
            print("********************************\n")
        else:
            print("Sleeping for", 10-processtime, "Seconds")
            print("********************************\n")
            time.sleep(10-processtime)

