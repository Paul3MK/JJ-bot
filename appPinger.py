import schedule
import time as uniqueTime
import urllib.request
from datetime import time, datetime
import os
import psycopg2

# def pingFunc():
#     #urllib.request.urlopen("https://jjbot-test.herokuapp.com/")
#     print("pinged your app")

# def keepOnlineFunc():
#     """This function is repsonsible for keeping the bot online (kinda like Pingdom or Kaffeine). It pings the app's domain every 29 minutes (because the apps on Heroku's free tier fall asleep after 30 minutes) by running the pingFunc function. This to minimise the bot's response time and to prevent db provisioning & dialogue training all the time"""
#     schedule.every(1).minutes.do(pingFunc)
#     schedule.run_pending()

def is_time_between(begin_time, end_time, check_time=None):
    """Checks what the time is"""
    # If check time is not given, default to current UTC time
    check_time = check_time or datetime.utcnow().time()
    if begin_time < end_time:
        return check_time >= begin_time and check_time <= end_time
    else: # crosses midnight
        return check_time >= begin_time or check_time <= end_time
    # returns True or False

while True: # this while block constantly checks what the time is, in order to keep pinging the app or not. Required because due to quotas, I only want 18 hours of app uptime per day (540 hours per month, as the limit is 550 hours/mo)
    if is_time_between(time(1,00), time(7,30)): # 6:30 of sleep is better 
        pass
    else:
        urllib.request.urlopen("https://jjbot-test.herokuapp.com/")
        print("pinged your app")
        uniqueTime.sleep(810)
    uniqueTime.sleep(60)
    