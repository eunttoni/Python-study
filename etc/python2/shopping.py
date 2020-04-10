from flask import Flask, render_template, jsonify, request
app = Flask(__name__)

from pymongo import MongoClient           # pymongo를 임포트 하기(패키지 인스톨 먼저 해야겠죠?)
client = MongoClient('localhost', 27017)  # mongoDB는 27017 포트로 돌아갑니다.
db = client.dbsparta                      # 'dbsparta'라는 이름의 db를 만듭니다.

## HTML을 주는 부분
@app.route('/')
def home():
    return render_template('hw01.html')

## API 역할을 하는 부분
@app.route('/order', methods=['POST'])
def write_order():
	# 1. 클라이언트가 준 주문정보 가져오기.
    userName_receive = request.form['userName_give']
    inputGroupSelect_receive = request.form['inputGroupSelect_give']
    address_receive = request.form['address_give']
    phone_receive = request.form['phone_give']
    

	# 2. DB에 정보 삽입하기
    doc = {
        'userName': userName_receive,
        'count' : inputGroupSelect_receive,
        'address': address_receive,
        'phone': phone_receive
    }
    db.shopping.insert_one(doc)
	# 3. 성공 여부 & 성공 메시지 반환하기

    return jsonify({'result': 'success', 'msg': '주문이 성공적으로 전송되었습니다.'})


@app.route('/order', methods=['GET'])
def read_orders():
    # 1. DB에서 리뷰 정보 모두 가져오기
    orderLists = list(db.shopping.find({}, {'_id': False}))
    # 2. 성공 여부 & 리뷰 목록 반환하기
    return jsonify({'result': 'success', 'orderLists': orderLists})


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)