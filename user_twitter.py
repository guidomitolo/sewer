import csv
from connection import TwitterConnect

api = TwitterConnect()

characters = ['alferdez', 'CFKArgentina','mariuvidal','mauriciomacri']

for character in characters:

    # the last 200
    tweets = api.user_timeline(
        id=character,
        exclude_replies=True, 
        include_rts=False, 
        tweet_mode = 'extended',
        count=200    
    )

    all_tweets = []
    all_tweets.extend(tweets)
    oldest_id = tweets[-1].id

    while len(tweets) != 0:
        oldest_id = tweets[-1].id
        tweets = api.user_timeline(
            id = character,
            count=200,
            include_rts = False,
            max_id = oldest_id - 1,
            tweet_mode = 'extended'
        )
        all_tweets.extend(tweets)

    with open(f'data/{character}_tweets.csv', mode='w') as data_tweets:
        data = csv.writer(data_tweets, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

        for tweet in all_tweets:
            data.writerow(
                [
                    tweet.user.name,
                    tweet.id_str, 
                    tweet.created_at, 
                    tweet.favorite_count, 
                    tweet.retweet_count, 
                    tweet.full_text.encode("utf-8").decode("utf-8")
                ]
            )