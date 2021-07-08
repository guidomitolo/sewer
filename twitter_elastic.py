from connection import TwitterConnect
import datetime

from model_elastic import elastic_connect, create_index

api = TwitterConnect()

# connect and create index if none
connection = elastic_connect()
create_index(connection)

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

        for i, tweet in enumerate(all_tweets):

            # check if retweet from retweet status
            try:
                tweet.retweeted_status
                retweeted = True
            except:
                retweeted = False

            insert = connection.index(
                index = 'twitter',
                id = i,
                body = {
                    'name': tweet.user.name,
                    'user_id': tweet.user.id,
                    'tweet_id': tweet.id_str, 
                    'date': tweet.created_at, 
                    'favs': tweet.favorite_count, 
                    'rts': tweet.retweet_count, 
                    'tweet': tweet.full_text.encode("utf-8").decode("utf-8"),
                    'reply': tweet.in_reply_to_user_id,
                    'quote': tweet.is_quote_status,
                    'retweet': retweeted
                }
            )