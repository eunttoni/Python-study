import requests

r = requests.get('http://openapi.seoul.go.kr:8088/6d4d776b466c656533356a4b4b5872/json/bikeList/1/99')
rjson = r.json()

# 102. 망원역 1번출구 앞 ( 9  /  22 )
# 망원역 1번출구 앞 ( 9  /  22 ) -> 문자열[숫자:] 숫자만큼 문자열의 앞부분을 잘라줌
# split('. ') -> 이렇게 사용해도 원하는 결과를 얻을 수 있다. 
for row in rjson['rentBikeStatus']['row']:
    print(row['stationName'][4:], "(", row['parkingBikeTotCnt'], "/", row['rackTotCnt'], ")")
