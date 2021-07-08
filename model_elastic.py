import requests
from elasticsearch import Elasticsearch

def elastic_connect():

    try:
        # Connect to the elastic cluster
        connect = Elasticsearch(
            [
                {
                    'host':'localhost',
                    'port':9200
                }
            ]
        )
        req = requests.get('http://localhost:9200')
        print(req)
        return connect
    except Exception as ex:
        print('Not Connected!')
        print(str(ex))
        return False


def create_index(es_object, index_name='twitter'):
    settings = {
        "settings": {
            "number_of_shards": 5,
            "number_of_replicas": 0
        },
        "mappings": {
            "properties": {
                "name": {
                    "type": "text"
                },
                "user_id": {
                    "type": "integer"
                },
                "tweet_id": {
                    "type": "text"
                },
                "date": {
                    "type": "date",
                    "format": "yyyy-MM-dd'T'HH:mm:ss"
                },
                "favs": {
                    "type": "integer"
                },
                "rts": {
                    "type": "integer"
                },
                "tweet": {
                    "type": "text"
                },
                "reply": {
                    "type": "text"
                },
                "quote": {
                    "type": "boolean"
                },
                "retweet": {
                    "type": "boolean"
                }
            }
        }
    }
    
    try:
        if not es_object.indices.exists(index_name):
            es_object.indices.create(
                index=index_name,
                ignore=400, 
                body=settings
                )
            print(f"'{index_name}' index created!")
        else:
            print(f"'{index_name}' index already created.")
    except Exception as ex:
        print(str(ex))