'''
가상환경 세팅 후에 터미널에서 아래 두 코드 실행하시면 됩니다!!
pip install flask
pip install flask_sqlalchemy
'''
from flask import Flask, render_template, request
import random
from flask_sqlalchemy import SQLAlchemy
import os



#########################################################
############# 파이썬 코드로 데이터베이스 다루기###################

# 플라스크와 데이터베이스 연결
basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = \
            'sqlite:///' + os.path.join(basedir, 'database.db')

db = SQLAlchemy(app)

# 테이블 생성 코드
class RockPaperSissor(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    com = db.Column(db.String(100), nullable=False)
    user = db.Column(db.String(100), nullable=False)
    result = db.Column(db.String(100), nullable=False)

    def __rerp__(self):
        return f'사용자 : {self.user} 컴퓨터 : {self.com} 결과 : {self.result}'
    

with app.app_context():
    db.create_all()

#################################################################
##################################################################

# @app.route("/")
@app.route("/", methods=["GET","POST"])
def home():

    ####### 코드 작성 ############
    rsp = ["가위", "바위", "보"]
    rsp_data = {} #데이터

    if request.method == "POST":
        #POST 방식으로 저장 할 경우 form.get
        # guest = request.form.get("rsp_guest") #게스트 input name="rsp_guest"
        guest = "가위"  # 임시
        bot = random.choice(rsp) #봇

        # 비겼습니다 졌습니다 이겼습니다 이 단어는 임의적 데이터
        if guest == bot:
            r = "비겼습니다"
        elif ((guest == "가위" and bot == "바위") or (guest == "바위" and bot == "보") or (guest == "보" and bot == "가위")):
            r = "졌습니다"
        else:
            r = "이겼습니다"

        gh = RockPaperSissor(user=guest, com=bot, result=r)
        db.session.add(gh)
        db.session.commit()

        # 임시
        q = RockPaperSissor.query.order_by(RockPaperSissor.id.desc()).all(); #오른찻순 수정

        # 임의적 메시지
        rsp_data["msg"] = f"사용자 : {guest} 컴퓨터 : {bot} {r}"
        rsp_data["gh"] = q

    return render_template("game.html", data=rsp_data)

if __name__ == '__main__':
    app.run(debug=True)
