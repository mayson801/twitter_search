import twitter
import csv
import operator
from textblob import TextBlob

# this is to connect to twitter these codes are on the twitter deleveloper page
api = twitter.Api(consumer_key='###################',
                  consumer_secret='#######################',
                  access_token_key='############################',
                  access_token_secret='#################################',
                  tweet_mode='extended',
                  sleep_on_rate_limit=True,
                  )

lasttweetId = 0
newstart = 0
i = 1
finished = False
file = "alibaba.csv"
opinion = 'null'
date = 'null'
retweet = False
tweetsformated = 'null'
tweettext = 'null'

with open(file, newline='', encoding='utf-8') as f:
    reader = csv.reader(f)
    sortedlist = sorted(reader, key=operator.itemgetter(4), reverse=True)
filename = file
 #opening the file with w+ mode truncates the file
f = open(filename, "w+")
f.close()

for tweet in sortedlist:
    with open(file, 'a', newline='', encoding='utf-8') as csvFile:
        writer = csv.writer(csvFile)
        writer.writerow(tweet)
    if lasttweetId == 0:
        print(tweet[4])
        lasttweetId = tweet[4]

while finished == False :
    # result is the variable for the search
    # the term is the search word @ get tweets @ at someone, count is how many tweets will be gathered up to a max of 100
    if newstart == 0:
        results = api.GetSearch(term="alibaba", count="100", result_type="recent", lang="en")
    else:
        results = api.GetSearch(term="alibaba", count="100", result_type="recent", lang="en", max_id=newstart)

    # this is used to determine if a tweet is negative,positive or neutral
    for tweet in results:
        # this gets the date by getting characters between 4 and 11 of the tweet.created_at to get the month and date
        # the + tweet.created_at[26:] gets the year
        date = tweet.created_at[4:11] + tweet.created_at[26:] + tweet.created_at[10:16]
        try:
            if tweet.retweeted_status:
                tweettext = TextBlob(tweet.retweeted_status.full_text)
                tweetsformated = str.join(" ", tweet.retweeted_status.full_text.splitlines())
                retweet = True
        except:
            tweettext = TextBlob(tweet.full_text)
            tweetsformated = str.join(" ", tweet.full_text.splitlines())
            tweettext = tweet.full_text
            retweet = False

        if tweettext.sentiment.polarity > 0:
            opinion = 'pos'
        elif tweettext.sentiment.polarity == 0:
            opinion = 'neut'
        else:
            opinion = 'neg'

        print(i, "date:", date, opinion, "Tweeted:", tweetsformated, "fav count:", tweet.favorite_count, tweet.id)
        row = [date, tweetsformated, opinion, tweettext.sentiment.polarity, tweet.id, tweet.favorite_count, retweet]
        with open(file, 'a', newline='', encoding='utf-8') as csvFile:
            writer = csv.writer(csvFile)
            writer.writerow(row)
        i = i + 1

    if newstart == tweet.id-1:
        finished = True
        print('tweets download finished')
    newstart = tweet.id - 1



