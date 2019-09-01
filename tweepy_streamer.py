from tweepy import API 
from tweepy import Cursor
from tweepy.streaming import StreamListener #permite 'ouvir' o twitter
from tweepy import OAuthHandler #permite autenticação do twitter app
from tweepy import Stream 

from textblob import TextBlob  # Para analise de sentimentos

import twitter_credentials  # Para credenciais do twitter
import numpy as np   # Para analisar os dados do twitter
import pandas as pd  # Para analisar os dados do twitter
import matplotlib.pyplot as plt  # Para gráficos
import re  # Para expressão regular

import json


# # # Twitter Client # # #
class TwitterClient():
    def __init__(self, twitter_user=None):
        # Objeto de autenticacao => auth 
        # Passa o auth para a API do twitter para que ele seja autenticado
        self.auth = TwitterAuthenticator().authenticate_twitter_app()
        self.twitter_client = API(self.auth)
        
        self.twitter_user = twitter_user

    
    def get_twitter_client_api(self):
        return self.twitter_client

    # Metodo para pegar os tweets(permitindo escolher a qtd de tweets que queremos extrair)
    def get_user_timeline_tweets(self, num_tweets):
        tweets = []
        # Pega o tweet da timeline do usuario do twitter . pega a qtd de tweets desejada
        # Adiciona cada tweet na lista de 
        # Especificando o usuario: id=self.twitter_user
        for tweet in Cursor(self.twitter_client.user_timeline, id=self.twitter_user).items(num_tweets):
            tweets.append(tweet)
        return tweets

    # Metodo para pegar os amigos do usuário(permitindo escolher a qtd de amigos que queremos pegar)
    def get_friend_list(self, num_friends):
        friend_list = []
        for friend in Cursor(self.twitter_client.user_timeline, id=self.twitter_user).items(num_friends):
            friend_list.append(friend)
        return friend_list

    # Metodo para pegar os tweets da home, das pessoas que você segue(permitindo escolher a qtd de tweets que queremos extrair)
    def get_home_timeline_tweets(self, num_tweets):
        home_timeline_tweets = []
        for tweet in Cursor(self.twitter_client.user_timeline, id=self.twitter_user).items(num_tweets):
            home_timeline_tweets.append(tweet)
        return home_timeline_tweets


# # # Twitter Authenticater # # #
class TwitterAuthenticator():

    def authenticate_twitter_app(self):
        auth = OAuthHandler(twitter_credentials.CONSUMER_KEY, twitter_credentials.CONSUMER_SECRET) #Consumer key
        auth.set_access_token(twitter_credentials.ACCESS_TOKEN, twitter_credentials.ACCESS_TOKEN_SECRET) #Access token
        return auth


# # # Twitter Streamer # # #
class TwitterStreamer():
    """
    Class for streaming and processing live tweets.
    Classe para processar tweets em tempo real.
    """
    def __init__(self):
        self.twitter_autenticator = TwitterAuthenticator()

    def stream_tweets(self, fetched_tweets_filename, hash_tag_list):
        # This handles Twitter authetification and the connection to Twitter Streaming API
        #Isso lida com a autenticação do twitter e a conexão da API do twitter
        listener = TwitterListener(fetched_tweets_filename) #como eu lido com os dados e com os tweets
        auth = self.twitter_autenticator.authenticate_twitter_app()
        stream = Stream(auth, listener)

        #palavras para filtrar no twitter
        stream.filter(track = hash_tag_list) 


# # # Twitter Stream Listener # # #
class TwitterListener (StreamListener):
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
        if status == 420:
            # Returna false no metodo on_data no caso do limite do twitter ocorra
            # O  twitter pode tirar o seu acesso caso você tente acessar algo além do limite
            # Quando você tenta fazer isso ele apresenta um erro "420"
            return False
        print(status)


# # # Tweet Analyzer # # #
class TweetAnalyzer():
    """
    Functionality for analyzing and categorizing content from tweets.
    """

    # Limpa o tweet com uma expressão regular
    def clean_tweet(self, tweet):
        return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split())

    def analyze_sentiment(self, tweet):
        analysis = TextBlob(self.clean_tweet(tweet))
        
        if analysis.sentiment.polarity > 0:  # Positivo
            return 1
        elif analysis.sentiment.polarity == 0:  # Neutro
            return 0
        else:  # Negativo
            return -1


    # Converte os tweets para data frame
    def tweets_to_data_frame(self, tweets):
        # Pega o text do tweet, e faz isso com todos os tweets (loop)
        df = pd.DataFrame(data=[tweet.text for tweet in tweets], columns=['tweets'])

        # Criando colunas no data frame
        # Fazendo um loop para cada tweet da lista de tweets
        #df['id'] = np.array([tweet.id for tweet in tweets])
        #df['len'] = np.array([len(tweet.text) for tweet in tweets])
        #df['date'] = np.array([tweet.created_at for tweet in tweets])
        #df['source'] = np.array([tweet.source for tweet in tweets])
        #df['likes'] = np.array([tweet.favorite_count for tweet in tweets])
        #df['retweets'] = np.array([tweet.retweet_count for tweet in tweets])

        return df


if __name__ == "__main__":
    # Palavras para filtrar no twitter
    hash_tag_list = ['xiaomi mi9']
    fetched_tweets_filename = "tweets.txt"

    # Printar a função de pegar tweets
    #print(twitter_client.get_user_timeline_tweets(1))

    twitter_streamer = TwitterStreamer()
    twitter_streamer.stream_tweets(fetched_tweets_filename, hash_tag_list)

    #twitter_client = TwitterClient()
    #tweet_analyzer = TweetAnalyzer()

    #api = twitter_client.get_twitter_client_api()
    
    # A função "user_timeline()" é uma função do tweepy API, já pronta do twitter client
    '''
    tweets = api.user_timeline(screen_name="realDonaldTrump", count=200)
    
    #tweets = twitter_streamer.filter(follow=None, track=hash_tag_list, languages=["pt"])

    df = tweet_analyzer.tweets_to_data_frame(tweets)
    df['sentiment'] = np.array([tweet_analyzer.analyze_sentiment(tweet) for tweet in df['tweets']])

    print(df.head(10))
    #print(df)
    '''
    
    '''
    #Alguns testes mostrando o que podemos extrair de cada tweet
    print(tweets)
    print(tweets[0])
    print(dir(tweets[0]))
    print(tweets[0].id)
    print(tweets[0].retweet_count)
    '''

    '''
    df = tweet_analyzer.tweets_to_data_frame(tweets)
    #print(df.head(10))
    #print(df)

    # Pega o tamanho médio de todos os tweets
    print(np.mean(df['len']))

    # Pega o número de likes do tweet mais curtido
    print(np.max(df['likes']))

    # Pega o número de retweets do tweet mais retweetado
    print(np.max(df['retweets']))

    # Time Series
    #time_likes = pd.Series(data=df['len'].values, index=df['date'])
    #time_likes.plot(figsize=(16, 4), color='r')
    #plt.show()
    
    #time_favs = pd.Series(data=df['likes'].values, index=df['date'])
    #time_favs.plot(figsize=(16, 4), color='r')
    #plt.show()

    #time_retweets = pd.Series(data=df['retweets'].values, index=df['date'])
    #time_retweets.plot(figsize=(16, 4), color='r')
    #plt.show()

    # Layered Time Series:
    #time_likes = pd.Series(data=df['likes'].values, index=df['date'])
    #time_likes.plot(figsize=(16, 4), label="likes", legend=True)

    #time_retweets = pd.Series(data=df['retweets'].values, index=df['date'])
    #time_retweets.plot(figsize=(16, 4), label="retweets", legend=True)
    #plt.show()
    '''

    