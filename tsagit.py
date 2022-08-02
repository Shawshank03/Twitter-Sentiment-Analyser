import sys
import csv
import tweepy
import matplotlib.pyplot as plt

from collections import Counter
from aylienapiclient import textapi  # (to analyze the sentiment of the Tweets)

if sys.version_info[0] < 3:
    input = raw_input

## Twitter credentials
# # Consume:
# CONSUMER_KEY    = "5JQDUi2sBBjpGSrwRYpN62jOp"
# CONSUMER_SECRET = "TPaF4taisrZKeDPYhaShJraPGWbzDWajk65CcNpoLWHMenKKgz"

# # Access:
# ACCESS_TOKEN  = "461231006-ybaeU47j2aBCRA9UNaVhbiKdNK7ugbDrFWoxd4Ra"
# ACCESS_SECRET = "FkcdxZGLL1i8y4tj3vpRFXrrWcmimBBthMMHMOJMJ8Zcg"
consumer_key = "5JQDUi2sBBjpGSrwRYpN62jOp"
consumer_secret = "TPaF4taisrZKeDPYhaShJraPGWbzDWajk65CcNpoLWHMenKKgz"
access_token = "461231006-ybaeU47j2aBCRA9UNaVhbiKdNK7ugbDrFWoxd4Ra"
access_token_secret = "FkcdxZGLL1i8y4tj3vpRFXrrWcmimBBthMMHMOJMJ8Zcg"

## AYLIEN credentials
application_id = "a0fbf0c1"
application_key = "0485c1dbab34d2cafd2dafdafab2875f"

## set up an instance of Tweepy
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

## set up an instance of the AYLIEN Text API
client = textapi.Client(application_id, application_key)

## search Twitter for something that interests you
query = input("What subject do you want to analyze for this example? \n")
number = input("How many Tweets do you want to analyze? \n")

results = api.search(
    lang="en",
    q=query + " -rt",
    count=number,
    result_type="recent"
)

print("--- Gathered Tweets \n")

## open a csv file to store the Tweets and their sentiment
file_name = 'Sentiment_Analysis_of_{}_Tweets_About_{}.csv'.format(number, query)

with open(file_name, 'w', newline='') as csvfile:
    csv_writer = csv.DictWriter(

        f=csvfile,
        fieldnames=["Tweet", "Sentiment"]
    )
    csv_writer.writeheader()

    print("--- Opened a CSV file to store the results of your sentiment analysis... \n")

    ## tidy up the Tweets and send each to the AYLIEN Text API
    for c, result in enumerate(results, start=1):
        tweet = result.text
        tidy_tweet = tweet.strip().encode('ascii', 'ignore')
        print("Analyzed Tweet {} \n".format(c))
        print(result.user,"\n",result.text,"\n\n")
        if len(tweet) == 0:
            print('Empty Tweet')
            continue

        response = client.Sentiment({'text': tidy_tweet})
        csv_writer.writerow({
            'Tweet': response['text'],
            'Sentiment': response['polarity']
        })


## count the data in the Sentiment column of the CSV file
with open(file_name, 'r') as data:
    counter = Counter()
    for row in csv.DictReader(data):
        counter[row['Sentiment']] += 1

    positive = counter['positive']
    negative = counter['negative']
    neutral = counter['neutral']

## declare the variables for the pie chart, using the Counter variables for "sizes"
colors = ['green', 'red', 'grey']
sizes = [positive, negative, neutral]
labels = 'Positive', 'Negative', 'Neutral'

## use matplotlib to plot the chart
plt.pie(
    x=sizes,
    autopct='%1.1f%%',
    colors=colors,
    labels=labels,
    startangle=90,
    explode = (0.2, 0, 0),
    shadow=True,

)

plt.title("Sentiment of {} Tweets about {}".format(number, query))
file_Savename = 'Sentiment_Analysis_of_{}_Tweets_About_{}.png'.format(number, query)
plt.savefig(file_Savename)
plt.show()