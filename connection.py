import os
from dotenv import load_dotenv
import tweepy as tw 

env_dir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(env_dir, '.env'))


def TwitterConnect():

    api_key = os.environ.get("API_KEY_TWITTER")
    api_secret_key = os.getenv('API_SECRET_KEY_TWITTER')
    token = os.getenv('ACCESS_TOKEN_TWITTER')
    token_secret = os.getenv('ACCESS_TOKEN_SECRET_TWITTER')

    auth = tw.OAuthHandler(api_key, api_secret_key)
    auth.set_access_token(token, token_secret)
    api = tw.API(auth, wait_on_rate_limit=True)

    try:
        api.verify_credentials()
        print("Authentication OK")
        return api
    except:
        print("Error during authentication")
        return False
