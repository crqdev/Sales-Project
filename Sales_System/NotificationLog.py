import config
import ast

class NotificationLog:
    @staticmethod
    def read():
        log = []
        try:
            f = open("notification.log", 'r')
            read_data = f.read().split("\n")
            for i in read_data:
                if i == "":
                    break
                log.append(ast.literal_eval(i))  # Convert String to Dict
            f.close()
            return log

        except FileNotFoundError:
            return []

    @staticmethod
    def write(Sales):
        try:
            f = open("notification.log", 'w')
            for i in Sales:
                f.write(str({"source": i["source"], "id": i["id"], "created_utc": i["created_utc"]})+"\n")
            f.close()

        except FileNotFoundError:
            print("Not Found")

    @staticmethod
    def clean(Sales, CurrentTime):
        newlog = []
        for i in Sales:
            if CurrentTime - i["created_utc"] <= config.Tracking_Time:
                newlog.append(i)

        return newlog

    @staticmethod
    def update_log(sales, currenttime):
        NotificationLog.write(NotificationLog.clean(sales, currenttime))