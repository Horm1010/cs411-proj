from django.shortcuts import render
from django.views.decorators import csrf
from django.http import QueryDict
from TestModel.models import Test_date
from TestModel.models import Test_tweet
from django.db.models import Q
import tweepy
import datetime
import xlsxwriter
import sys

def run(start_y, start_m,start_d,end_y,end_m,end_d, date_x):
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
        if tweet.created_at < endDate and tweet.created_at > startDate and tweet.created_at not in date_x:
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


def cache(start_y,start_m,start_d,end_y,end_m,end_d):
    startDate = datetime.datetime(start_y, start_m, start_d, 0, 0, 0)
    endDate =   datetime.datetime(end_y, end_m, end_d, 0, 0, 0)

    try:
        condition_1 = Q(date__gte = startDate)
        condition_2 = Q(date__lte = endDate)
        dates = list(Test_date.objects.filter(condition_1 & condition_2))
    except Test_date.DoesNotExist:
        #find all tweets from remote server when tweets within required date are not in cache
        tweets = run(start_y,start_m,start_d,end_y,end_m,end_d, [])
        # insert tweets into cache
        for ts in tweets:
            a = Test_date(date = ts.created_at)
            a.save()
            Test_date.objects.order_by(date)
            b = Test_tweet(id = ts.id, date = a, tweet = ts.text)
            b.save()
            Test_tweet.objects.order_by(id)
        return tweets
    # find tweets from remote server which are not in local cache
    tweets = run(start_y,start_m,start_d,end_y,end_m,end_d, dates)
    # find tweets in cache
    for i in dates:
        t = list(Test_date.objects.filter(date = i))
        tweets = tweets + t
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
        #check the cache
        tweets = cache(start_y,start_m,start_d,end_y,end_m,end_d)
        ctx['item_list'] = tweets
    return render(request, "search.html", ctx)
