import config


def reddit_threshold(data):
    posts = []

    if data == []:
        return  posts

    for i in data:
        if int(i["score"]) >= config.reddit_min_upvotes:
            posts.append(i)
    return posts


def SD_threshold(data):
    posts = []
    if data == []:
        return  posts

    for i in data:
        if int(i["views"]) > config.SD_views_min and int(i["timealive"]) <= config.SD_alive_min and int(i["score"]) >= 0:
            posts.append(i)

        elif int(i["views"]) > config.SD_views_mid and int(i["timealive"]) <= config.SD_alive_mid and int(i["score"]) >= 0:
            posts.append(i)

        elif int(i["views"]) > config.SD_views_high and int(i["timealive"]) <= config.SD_alive_high and int(i["score"]) >= 0:
            posts.append(i)
    return posts


