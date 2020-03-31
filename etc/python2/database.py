# import pymongo
# pymongo룰 import했다.
from pymongo import MongoClient           # pymongo를 임포트 하기(패키지 인스톨 먼저 해야겠죠?)
# pymongo 안에 있는 MongoClient를 import했다.
client = MongoClient('localhost', 27017)  # mongoDB는 27017 포트로 돌아갑니다.
db = client.dbsparta                      # 'dbsparta'라는 이름의 db를 만듭니다.
# 없는 걸 사용하는데... 자동으로 생성해준다.

# MongoDB에 insert 하기

# 'users'라는 collection에 {'name':'bobby','age':21}를 넣습니다.
# client.dbsparta.users.insert_one({'name':'bobby','age':21})
# 위와 같은 형태로도 사용할 수 있다.
# db.users.insert_one({'name':'bobby','age':21})
# insert , insert_one
all_users = list(db.users.find({'age':21}))
# find , find_one
# print(all_users[0])
# for user in all_users:
#     print(user['name']," : ",user['age'])

db.users.update_one({'name':'bobby'},{'$set':{'age':27}})
