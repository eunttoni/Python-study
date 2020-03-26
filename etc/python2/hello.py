import requests  # requests 라이브러리 설치 필요

r = requests.get('http://openapi.seoul.go.kr:8088/6d4d776b466c656533356a4b4b5872/json/RealtimeCityAir/1/99')
rjson = r.json()

# 파이썬에서 함수 만들기
def name(a):
    print(a)

# ctrl + alt + l : 코드 정리 해줌
name("시작")

for row in rjson['RealtimeCityAir']['row']:
    # 0.03 이상인 것만 출력
    if row['NO2'] >= 0.03:
        print(row['MSRSTE_NM'], " : ", row['NO2'])

name("끝")



# 불린은 대문자로 시작함
# a = True
# b = False

# print (rjson['RealtimeCityAir']['row'][0]['NO2'])
# a = {
#     "data" : [
#         {"a" : 1, "B" : 2},
#         {"a" : 2, "B" : 3},
#         {"a" : 3, "B" : 4}
#     ]
# }
#
# print(a['data'][1]["B"])
