import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient

client = MongoClient('localhost',27017)
db = client.dbsparta.mask

def scrap_and_insert():
    headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
    r = requests.get('https://8oi9s0nnth.apigw.ntruss.com/corona19-masks/v1/stores/json',headers=headers)
    rjson = r.json()

    for row in rjson['storeInfos']:
        print(row['name'], row['type'], row['addr'], row['code'], row['lat'], row['lng'])
        data = {'name': row['name'] , 'addr' : row['addr'] , 'type' : row['type'] ,
                'code' : row['code'] , 'lat' : row['lat'] , 'lng' : row['lng']}
        db.insert_one(data)

def find_and_print():
    all_movies = list(db.find())
    for movie in all_movies:
        print(movie['name'], " : ", movie['addr'])

find_and_print()



