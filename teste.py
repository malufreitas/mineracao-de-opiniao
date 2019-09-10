# YouTube Video: https://www.youtube.com/watch?v=wlnx-7cm4Gg
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import json

import twitter_credentials

# # # # TWITTER STREAM LISTENER # # # #
class StdOutListener(StreamListener):
    def __init__(self, fetched_tweets_filename):
        self.fetched_tweets_filename = fetched_tweets_filename

    def on_data(self, data):
        try:
            '''
            tweet = json.loads(data)
            created_at = tweet["created_at"]
            id_str = tweet["id_str"]
            text = tweet["text"]
            obj = {"created_at":created_at,"id_str":id_str,"text":text,}
            
            print(obj)
            '''
            print(data)

            with open(self.fetched_tweets_filename, 'a') as tf:
                tf.write(data)
            return True
        
        except BaseException as e:
            print("Error on_data %s" % str(e))
        return True

    def on_error(self, status):
        print(status)

if __name__ == "__main__":
    fetched_tweets_filename = "tweets.csv"
    hash_tag_list = ["amazon prime"]

    listener = StdOutListener(fetched_tweets_filename)

    auth = OAuthHandler(twitter_credentials.CONSUMER_KEY, twitter_credentials.CONSUMER_SECRET)
    auth.set_access_token(twitter_credentials.ACCESS_TOKEN, twitter_credentials.ACCESS_TOKEN_SECRET)

    stream = Stream(auth, listener)

    stream.filter(track=hash_tag_list)