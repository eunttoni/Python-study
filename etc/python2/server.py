from flask import Flask, render_template

app = Flask(__name__)
# Flask('내 서버')

# {{ url_for('static', filename='css/mystyle.css') }}

@app.route('/')
def home():
   return render_template('hw01.html')

@app.route('/mypage')
def mypage():
   return 'This is My Page!'

# 너 실행했니? 물어보는거라 없어도 상관없는 조건이다.
# 아래 한 줄만 써놔도 무관.
if __name__ == '__main__':
   app.run('0.0.0.0',port=5000,debug=True)