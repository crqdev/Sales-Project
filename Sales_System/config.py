# Reddit Details
reddit_username = ""
reddit_password = ""
reddit_client_id = ""
reddit_client_secret = ""
reddit_agelimit = 400  # Only Extract Posts Below X Seconds Old
reddit_min_upvotes = 3

# SlickDeals Details
SD_Timezone = 14400  # Put Down Difference in seconds between your timezone and UTC
SD_agelimit = 1800   # Only Extract Posts Below X Seconds Old

SD_views_min = 10
SD_views_mid = 20
SD_views_high = 100

SD_alive_min  = 200
SD_alive_mid = 500
SD_alive_high = 900


# SD Categories (Only Popular Ones)
# Add More Categories or change values
# You will be sent notifications with keys that have a True Value

Category_Screen = {"Home": False,
                   "Electronics": True,
                   "Other": False,
                   "Computers": True,
                   "Apparel": False,
                   "Kids": False,
                   "Games": True,
                   "Audio": True,
                   "Sport": False,
                   "Food": False,
                   "Beauty": False,
                   "Phone": True,
                   "Grocery": False,
                   "Travel": False,
                   "Auto": False,
                   "Tools": False,
                   "Games": False,
                   "Photo": False}

# Passes all other categories not in Category Screen if set true
PASS_ALL_OTHER_CATEGORIES = True

#PushBullet
PushBullet_API_KEY = ""

# Log Settings
Tracking_Time = 3600*4  # Seconds to Track Post in Log; MUST BE > either age Limit
