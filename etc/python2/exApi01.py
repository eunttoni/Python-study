import requests
from pymongo import MongoClient

client = MongoClient('localhost',27017)
db = client.dbsparta.bike

r = requests.get('http://openapi.seoul.go.kr:8088/6d4d776b466c656533356a4b4b5872/json/bikeList/1/99')
rjson = r.json()

# 102. 망원역 1번출구 앞 ( 9  /  22 )
# 망원역 1번출구 앞 ( 9  /  22 ) -> 문자열[숫자:] 숫자만큼 문자열의 앞부분을 잘라줌
# split('. ') -> 이렇게 사용해도 원하는 결과를 얻을 수 있다. 
# for row in rjson['rentBikeStatus']['row']:
#     print(row['stationName'][4:], "(", row['parkingBikeTotCnt'], "/", row['rackTotCnt'], ")")
    # db.insert_one({'stationName':row['stationName'][4:], 'parkingBikeTotCnt':row['parkingBikeTotCnt'], 'rackTotCnt':row['rackTotCnt']})


def find_and_print():
    all_bike = list(db.find())
    for bike in all_bike:
        print(bike['stationName'])

find_and_print()