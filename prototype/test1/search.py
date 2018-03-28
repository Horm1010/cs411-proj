from django.shortcuts import render
from django.views.decorators import csrf
from django.http import QueryDict
import tweepy
import datetime
import xlsxwriter
import sys

def run(start_y, start_m,start_d,end_y,end_m,end_d):
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
    startDate = datetime.datetime(start_y, start_m, start_d, 0, 0, 0)
    endDate =   datetime.datetime(end_y, end_m, end_d, 0, 0, 0)
    
    tweets = []
    tmpTweets = api.user_timeline(username)
    for tweet in tmpTweets:
        if tweet.created_at < endDate and tweet.created_at > startDate:
            tweets.append(tweet)

    while (tmpTweets[-1].created_at > startDate):
        #print("Last Tweet @", tmpTweets[-1].created_at, " - fetching some more")
        tmpTweets = api.user_timeline(username, max_id = tmpTweets[-1].id)
        for tweet in tmpTweets:
            if tweet.created_at < endDate and tweet.created_at > startDate:
                tweets.append(tweet)

    workbook = xlsxwriter.Workbook(username + ".xlsx")
    worksheet = workbook.add_worksheet()
    row = 0
    for tweet in tweets:
        worksheet.write_string(row, 0, str(tweet.id))
        worksheet.write_string(row, 1, str(tweet.created_at))
        worksheet.write(row, 2, tweet.text)
        worksheet.write_string(row, 3, str(tweet.in_reply_to_status_id))
        row += 1

    workbook.close()
    return tweets

# request post
def search_post(request):
    
    ctx ={}
    if request.POST:
        start_y = int(request.POST.get('start_y'))
        start_m = int(request.POST.get('start_m'))
        start_d = int(request.POST.get('start_d'))
        end_y = int(request.POST.get('end_y'))
        end_m = int(request.POST.get('end_m'))
        end_d = int(request.POST.get('end_d'))
        tweets = run(start_y,start_m,start_d,end_y,end_m,end_d)
        ctx['item_list'] = tweets
    return render(request, "search.html", ctx)
