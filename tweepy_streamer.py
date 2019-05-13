from tweepy.streaming import StreamListener #permite 'ouvir' o twitter
from tweepy import OAuthHandler #permite autenticação do twitter app
from tweepy import Stream 

import twitter_credentials

class TwitterStreamer():
    """
    Class for streaming and processing live tweets.
    Classe para processar tweets em tempo real.
    """
    def stream_tweets(self, fetched_tweets_filename, hash_tag_list):
        # This handles Twitter authetification and the connection to Twitter Streaming API
        #Isso lida com a autenticação do twitter e a conexão da API do twitter
        listener = StdOutListener(fetched_tweets_filename) #como eu lido com os dados e com os tweets
        auth = OAuthHandler(twitter_credentials.CONSUMER_KEY, twitter_credentials.CONSUMER_SECRET) #Consumer key
        auth.set_access_token(twitter_credentials.ACCESS_TOKEN, twitter_credentials.ACCESS_TOKEN_SECRET) #Access token

        stream = Stream(auth, listener)

        #palavras para filtrar no twitter
        stream.filter(track = hash_tag_list) 


class StdOutListener (StreamListener):
    """
    This is a basic listener that just prints received tweets to stdout.
    Este é um ouvinte básico que apenas imprime tweets recebidos para stdout.
    """
    def __init__(self, fetched_tweets_filename):
        self.fetched_tweets_filename = fetched_tweets_filename

    def on_data(self, data):
        try:
            print(data)
            #reescrever escrever em arquivo
            with open(self.fetched_tweets_filename, 'a') as tf:
                tf.write(data)
            return True
        except BaseException as e:
            print("Error on_data %s" % str(e))

    def on_error(self, status):
        print(status)

if __name__ == "__main__":
    #palavras para filtrar no twitter
    hash_tag_list = ['xiaomi']
    
    fetched_tweets_filename = "tweets.json"
    #fetched_tweets_filename = "teste.json"

    twitter_streamer = TwitterStreamer()
    twitter_streamer.stream_tweets(fetched_tweets_filename, hash_tag_list)