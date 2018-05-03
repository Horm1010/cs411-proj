# -*- coding: utf-8 -*-
"""
Created on Thu May  3 00:33:45 2018

@author: Joe Keezy
"""

import tweepy
import datetime
import xlsxwriter
import sys

# credentials from https://apps.twitter.com/
consumerKey = "R7M9ual1AMtUDLGckATw8uI5G"
consumerSecret = "QUEYxWVFmj4kmUoGKNl8DIMAslpxBavgh8gKlQu1RnfjPvyK7s"
accessToken = "636562123-2OsKE5BXBwFzGM7NtE8MsSi2PI4zMy47wjusfZYE"
accessTokenSecret = "1WxOTBROUrUPJlkG3kRlZhvQi95h5RlWobimWKdiLcjXw"

auth = tweepy.OAuthHandler(consumerKey, consumerSecret)
auth.set_access_token(accessToken, accessTokenSecret)

api = tweepy.API(auth)

username = "realDonaldTrump"
#give todays tweets
startDate = datetime.datetime(2018, 1, 2, 0, 0, 0)
endDate =   datetime.datetime(2018, 1, 3, 0, 0, 0)

tweets = []
#needed to use extended tweet mode because of change to tweet size limit
tmpTweets = api.user_timeline(username, tweet_mode='extended')
for tweet in tmpTweets:
    if tweet.created_at < endDate and tweet.created_at > startDate:
        tweets.append(tweet)

while (tmpTweets[-1].created_at > startDate):
    #print("Last Tweet @", tmpTweets[-1].created_at, " - fetching some more")
    tmpTweets = api.user_timeline(username, max_id = tmpTweets[-1].id, tweet_mode='extended')
    for tweet in tmpTweets:
        if tweet.created_at < endDate and tweet.created_at > startDate:
            tweets.append(tweet)

#added in the startDate to the label for easy searching
workbook = xlsxwriter.Workbook(username + str(startDate)[0:10] + ".xlsx")
worksheet = workbook.add_worksheet()
row = 0
for tweet in tweets:
    worksheet.write_string(row, 0, str(tweet.id))
    worksheet.write_string(row, 1, str(tweet.created_at))
    #need full_text for the new character limit to be reached.
    worksheet.write(row, 2, tweet.full_text)
    worksheet.write_string(row, 3, str(tweet.in_reply_to_status_id))
    row += 1

workbook.close()