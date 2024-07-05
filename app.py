'''
가상환경 세팅 후에 터미널에서 아래 두 코드 실행하시면 됩니다!!
pip install flask
pip install flask_sqlalchemy
'''
from flask import Flask, render_template, request
import random
from flask_sqlalchemy import SQLAlchemy
import os
import urllib.parse

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
    id = db.Column(db.Integer, primary_key=True)
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
@app.route("/", methods=["GET", "POST"])
def home():
    ####### 코드 작성 ############
    rsp = ["가위", "바위", "보"]
    rsp_data = {}  # 데이터

    # q = 0
    t = 0
    # w = 0
    # l = 0
    # d = 0

    if request.method == "POST":
        # POST 방식으로 저장 할 경우 form.get
        guest = request.form.get("guest")  # 게스트 input name="guest"
        if guest is None:
            return "guest 파라미터가 없음"
        bot = random.choice(rsp)  # 봇


        if guest == bot:
            r = "무"
            r_msg = "비겼습니다."
        elif ((guest == "가위" and bot == "바위") or (guest == "바위" and bot == "보") or (guest == "보" and bot == "가위")):
            r = "패"
            r_msg = "졌습니다."
        else:
            r = "승"
            r_msg = "이겼습니다."

        #디비 입력
        gh = RockPaperSissor(user=guest, com=bot, result=r)
        db.session.add(gh)
        db.session.commit()

        # q = RockPaperSissor.query.order_by(RockPaperSissor.id.desc()).all()  # 오름찾순 리스트
        t = RockPaperSissor.query.order_by(RockPaperSissor.id.desc()).count()  # 플레이어 횟수
        # w = RockPaperSissor.query.filter_by(result="승").count() #승 갯수
        # l = RockPaperSissor.query.filter_by(result="패").count() #패 갯수
        # d = RockPaperSissor.query.filter_by(result="무").count() #무 갯수

        rsp_data["msg"] = r_msg
        rsp_data["guest"] = guest
        rsp_data["bot"] = bot
        # rsp_data["gh"] = q
        rsp_data["total"] = t
        # rsp_data["win"] = w
        # rsp_data["lose"] = l
        # rsp_data["draw"] = d

    return render_template("game.html", data=rsp_data)
    # return render_template("game.html")


if __name__ == '__main__':
    app.run(debug=True)
