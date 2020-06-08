import pandas as pd
import re
import numpy as np
import requests
from datetime import datetime
from bs4 import BeautifulSoup
from flask import Flask, render_template, jsonify, request
import json
app = Flask(__name__)


# auth = requests.get(
#     'https://sgisapi.kostat.go.kr/OpenAPI3/auth/authentication.json?consumer_key=e377e5b27bc940eebd3d&consumer_secret=006fb7b158554f96bb2c')
# authJson = auth.json()
# accessTimeout = authJson['result']['accessTimeout']
# accessToken = authJson['result']['accessToken']


def get_areacode():
    df_areacode = pd.read_csv('https://goo.gl/tM6r3v',
                              sep='\t', dtype={'법정동코드': str, '법정동명': str})
    df_areacode = df_areacode[df_areacode['폐지여부'] == '존재']
    df_areacode = df_areacode[['법정동코드', '법정동명']]
    return df_areacode


def get_province():
    # 전체 법정동명으로 법정동코드 검색
    df_areacode = get_areacode()
    df_province = df_areacode[df_areacode['법정동코드'].str.contains('\d{10}')]
    return df_province


@app.route('/realasset', methods=['POST'])
def get_naver_realasset():

    area_code = request.form['code']
    rletTypeCd = request.form['rletTypeCd']

    # rletTypeCd: A01=아파트, A02=오피스텔, B01=분양권, 주택=C03, 토지=E03,
    # 원룸=C01, 상가=D02, 사무실=D01, 공장=E02, 재개발=F01, 건물=D03
    # tradeTypeCd (거래종류): all=전체, A1=매매, B1=전세, B2=월세, B3=단기임대
    # hscpTypeCd (매물종류): 아파트=A01, 주상복합=A03, 재건축=A04 (복수 선택 가능)
    # cortarNo(법정동코드): (예: 1168010600 서울시, 강남구, 대치동)

    url = 'http://land.naver.com/article/articleList.nhn?' \
        + 'rletTypeCd=' + rletTypeCd + '&tradeTypeCd=A1&hscpTypeCd=' \
        + '&cortarNo=' + area_code

    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')

    table = soup.find('table')
    trs = table.tbody.find_all('tr')

    value_list = []

    # 거래, 종류, 확인일자, 매물명, 매물명, 면적(㎡), 층, 매물가(만원), 연락처
    for tr in trs[::2]:
        tds = tr.find_all('td')
        cols = [' '.join(td.text.strip().split()) for td in tds]

        if len(tds) < 3:
            continue

        if '_thumb_image' not in tds[3]['class']:  # 현장확인 날짜와 이미지가 없는 행
            cols.insert(3, '')

        deal = cols[0]  # 거래
        category = cols[1]  # 종류
        confirmDate = datetime.strptime(cols[2], '%y.%m.%d.')  # 확인일자
        현장확인 = cols[3]
        nameOfSale = cols[4].replace('네이버부동산에서 보기', '')   # 매물명
        면적 = cols[5]

        supplyArea = re.findall('공급면적(.*?)㎡', 면적)
        if len(supplyArea) == 0:
            supplyArea = re.findall('계약면적(.*?)㎡', 면적)    # 오피스텔의 경우 계약면적 제공
            if len(supplyArea) == 0:
                # 주택의 경우 공급면적 or 대지면적 제공
                supplyArea = re.findall('대지면적(.*?)㎡', 면적)
        supplyArea = supplyArea[0].replace(',', '')  # 공급면적 or 계약면적 or 대지면적

        exclusiveArea = re.findall('전용면적(.*?)㎡', 면적)
        if len(exclusiveArea) == 0:
            exclusiveArea = re.findall(
                '연면적(.*?)㎡', 면적)  # 주택의 경우 전용면적 or 연면적 제공
        exclusiveArea = exclusiveArea[0].replace(',', '')  # 전용면적 or 연면적

        supplyArea = float(supplyArea)
        exclusiveArea = float(exclusiveArea)
        floor = cols[6]    # 층
        price = int(cols[7].replace(',', ''))  # 매물가
        # 연락처 = cols[8]

        value_list.append(
            [deal, category, confirmDate, nameOfSale, supplyArea, exclusiveArea, floor, price])

    cols = ['거래', '종류', '확인일자', '매물명',
            '공급면적', '전용면적', '층', '매물가']
    df = pd.DataFrame(value_list, columns=cols)

    detection_json = df.to_json(orient='records', date_format="iso")

    json_dict = {}
    json_dict['data'] = json.loads(detection_json)

    # print(json_dict)

    return jsonify(json_dict)

# HTML을 주는 부분
@app.route('/')
def home():
    # r = requests.get(
    #     'https://sgisapi.kostat.go.kr/OpenAPI3/addr/stage.json?accessToken='+accessToken+'&pg_yn=0&cd=11')
    # rjson = r.json()
    # for row in rjson['result']:
    # print(row['full_addr'],  row['addr_name'], "/", row['cd'])
    # guList=rjson['result']
    return render_template('index.html')


@app.route('/searchCortar', methods=['POST'])
def searchCortar():
    inputText = request.form['inputText']

    # print("inputText ::::::::::::::::::: ", inputText)
    df_province = get_province()
    cortarNo = df_province.loc[df_province['법정동명']
                               == inputText, '법정동코드'].values[0]
    # print("cortarNo ::::::::::::::::::: ", cortarNo)

    return jsonify({'result': 'success', 'cortarNo': cortarNo})


``


@app.route('/dongList', methods=['POST'])
def dongList():
    cd = request.form['cd']
    r = requests.get(
        'https://sgisapi.kostat.go.kr/OpenAPI3/addr/stage.json?accessToken='+accessToken+'&pg_yn=0&cd='+cd)
    rjson = r.json()

    for row in rjson['result']:
        print(row['addr_name'], "/", row['cd'])

    return jsonify({'result': 'success', 'dongList': rjson['result']})


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
