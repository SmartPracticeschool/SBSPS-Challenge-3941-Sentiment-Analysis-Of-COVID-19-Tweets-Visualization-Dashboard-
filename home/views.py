import re

from django.shortcuts import render
import requests
from bs4 import BeautifulSoup

import csv
import tweepy
import re
from textblob import TextBlob



# Create your views here.
def home(request):
    actives = []
    cure = []
    deaths = []
    migr = []
    time = []
    URL = 'https://www.mohfw.gov.in/'
    extract_contents = lambda row: [x.text.replace('\n', '') for x in row]

    try:
        active = []
        cured = []
        death = []
        mig = []
        time_update = []
        t=[]
        a=[]
        c=[]
        d=[]
        m=[]
        current=active
        print(current)
        response = requests.get(URL).content
        soup = BeautifulSoup(response, 'html.parser')
        header = extract_contents(soup.tr.find_all('th'))
        for div in soup.findAll('div', attrs={'class': 'status-update'}):
            time_update.append(div.text.strip())
            t.append(time_update[0].replace("\n", " ")[0:14])
            t.append(time_update[0].replace("\n", " ")[15:])

        for div in soup.findAll('li', attrs={'class': 'bg-blue'}):
            active.append(div.text.strip())
            a.append(active[0].replace("\n", " "))
        for div in soup.findAll('li', attrs={'class': 'bg-green'}):
            cured.append(div.text.strip())
            c.append(cured[0].replace("\n", " ")[0:23])
        for div in soup.findAll('li', attrs={'class': 'bg-red'}):
            death.append(div.text.strip())
            d.append(death[0].replace("\n", " "))
        for div in soup.findAll('li', attrs={'class': 'bg-orange'}):
            mig.append(div.text.strip())
            m.append(mig[0].replace("\n", " "))
        stats = []
        all_rows = soup.find_all('tr')
        for row in all_rows:
            stat = extract_contents(row.find_all('td'))
            stats.append(stat)





    except Exception as e:
        print(e)

    time = t
    actives=a
    deaths=d
    cure=c
    migr=m
    #print(stats)
    last = list(stats[38:43])
    stats=stats[1:38]

    #print(last)

    return render(request,'home.html',{'time':time,'cure':cure,'deaths':deaths,'actives':actives,'last':last,'migr':migr,'stats':stats})



def senti(request):
    consumer_key="MV7mO4kcvb5vfT37D1SleIvjP"
    consumer_secret="ZEFUhWnfxHt8FHIiE30uj2VHSoTWCkJyHizmZPJoaY9PetSe3n"
    access_token="1239788459574702081-4821HJoOqWgLRuJlkchCtv36tw19PN"
    access_token_secret="qNYQ346ztGagyUuFUzIrf6fEZiICYgA1fg263W4WQmnrO"
    auth=tweepy.OAuthHandler(consumer_key,consumer_secret)
    auth.set_access_token(access_token,access_token_secret)
    api=tweepy.API(auth)

    def clean_tweet( tweet):
            return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split())

    def get_tweet_sentiment(tweet):
            analysis = TextBlob(clean_tweet(tweet))
            if analysis.sentiment.polarity > 0:
                return 100
            elif analysis.sentiment.polarity == 0:
                return 50
            else:
                return 0

    parsed_tweet = {}
    twee={}
    sentiment=[]
    val=[]

    def search_tweets(tweet):
        po = 0
        neu = 0
        neg = 0
        public_tweet = api.search(tweet, count=100, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)
        for i in public_tweet:
            parsed_tweet['text'] = i.text
            parsed_tweet['user'] = i.user.screen_name
            parsed_tweet['sentiment'] = get_tweet_sentiment(i.text)
            sen = get_tweet_sentiment(i.text)
            if sen == 100:
                po += 1
            if sen == 0:
                neg += 1
            if sen == 50:
                neu += 1


            twee[parsed_tweet['text']]=parsed_tweet['sentiment']

            sentiment.append( parsed_tweet['sentiment'])
            #print(parsed_tweet['user'])
            #print(parsed_tweet['text'])
            #print(parsed_tweet['sentiment'])
            #print("---------------------------------------------------------------------------")
        val.append(po)
        val.append(neg)
        val.append(neu)

    search_tweets("corona")
    print(val)
    context={'twee':twee,'sentiment':sentiment,'val': val}
    #print(sentiment)
    return render(request,'senti.html',context)