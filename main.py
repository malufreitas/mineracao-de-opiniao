# Instala o pacote tweepy
# $pip install tweepy

# Importando os módulos Tweepy, Datetime e Json
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
from datetime import datetime
from pymongo import MongoClient  # Importando do PyMongo o módulo MongoClient
import json

# Criando uma classe para capturar os stream de dados do Twitter e 
# armazenar no MongoDB
class MyListener(StreamListener):
    def on_data(self, dados):
        tweet = json.loads(dados)
        created_at = tweet["created_at"]
        id_str = tweet["id_str"]
        text = tweet["text"]
        obj = {"created_at":created_at,"id_str":id_str,"text":text}
        #tweetind = 
        col.insert_one(obj).inserted_id
        print(obj)
        return True


if __name__ == "__main__":
    # Chaves e tokens tirados da api do twitter
    consumer_key = "D7WbZKB1D8sI6SG5YSJaoUqFw"
    consumer_secret = "Ce2wShKqGIeMgHrmugmpNRK1AAGNXik1imJ47sLJnF4dhFKLqT"
    access_token = "758066017742512128-UaPf9IJfaJ957JO5nb4F8TNVa7PBH3p"
    access_token_secret = "amPLoPVU6hyOXUyNVRRVrzZPU6zP0lT8Mnt7eLxhbFzdF"

    # Criando as chaves de autenticação
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)


    # Criando o objeto mylistener
    mylistener = MyListener()

    # Criando o objeto mystream
    mystream = Stream(auth, mylistener)


    ### Preparando a Conexão com o MongoDB ###

    # Criando a conexão ao MongoDB
    client = MongoClient('localhost', 27017)

    # Criando o banco de dados twitterdb
    db = client.twitterdb

    # Criando a collection "col"
    col = db.tweets

    # Criando uma lista de palavras chave para buscar nos Tweets
    #keywords = ['Big Data', 'Python', 'Data Mining', 'Data Science']
    keywords = ['mulher na ti', 'mulher na computação', 'mulheres na ti', 'mulheres na computação']

    ### Coletando os Tweets ###

    # Iniciando o filtro e gravando os tweets no MongoDB
    mystream.filter(track=keywords)

    ## Consultando os Dados no MongoDB
    #mystream.disconnect()

    # Verificando um documento no collection
    #col.find_one()