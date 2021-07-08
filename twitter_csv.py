import csv
from connection import TwitterConnect
import datetime

api = TwitterConnect()

characters = ['alferdez', 'CFKArgentina','mariuvidal','mauriciomacri','elisacarrio','SergioMassa','horaciorlarreta']
users = []

for character in characters:

    # the last 200
    tweets = api.user_timeline(
        id=character,
        exclude_replies=False, 
        include_rts=True, 
        tweet_mode = 'extended',
        count=200    
    )
    
    user = [tweets[-1].user.name, tweets[-1].user.followers_count, tweets[-1].user.statuses_count, tweets[-1].user.created_at,  datetime.datetime.now()]
    users.append(user)

    all_tweets = []
    all_tweets.extend(tweets)
    oldest_id = tweets[-1].id

    while len(tweets) != 0:
        oldest_id = tweets[-1].id
        tweets = api.user_timeline(
            id = character,
            count=200,
            include_rts = True,
            exclude_replies=False, 
            max_id = oldest_id - 1,
            tweet_mode = 'extended'
        )
        all_tweets.extend(tweets)

    with open(f'data/{character}_tweets.csv', mode='w') as data_tweets:
        data = csv.writer(data_tweets, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

        for tweet in all_tweets:

            # check if retweet from retweet status
            try:
                tweet.retweeted_status
                retweeted = True
            except:
                retweeted = False

            data.writerow(
                [
                    tweet.user.name,
                    tweet.user.id,
                    tweet.id_str, 
                    tweet.created_at, 
                    tweet.favorite_count, 
                    tweet.retweet_count, 
                    tweet.full_text.encode("utf-8").decode("utf-8"),
                    tweet.in_reply_to_user_id,
                    tweet.is_quote_status,
                    retweeted
                ]
            )

with open(f'data/user_info.csv', mode='w') as user_info:
    data = csv.writer(user_info, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    data.writerows(users)