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

def rock_paper_sissor(player, computer):
    # print(f"사용자: {player}, 컴퓨터: {computer}")
    if player == computer:
        return "무승부"
    elif (player == '가위' and computer == '보') | (player == '바위' and computer == '가위') | (player == '보' and computer == '바위'):
        return "승리"
    else:
        return "패배"



@app.route("/")
def home():

    player = request.args.get("userchoice")
    computer = ""
    game_result = ""

    # print(player)
    
    if player == "reset":
        # 데이터베이스 초기화
        db.session.query(RockPaperSissor).delete()
        db.session.commit()
    


    if player in ["가위","바위","보"]:
        computer = random.choice(["가위","바위","보"])
        game_result = rock_paper_sissor(player,computer)
        
        # 데이터베이스에 저장
        rps = RockPaperSissor(com=computer, user=player, result=game_result)
        db.session.add(rps)
        db.session.commit()


    record_list = RockPaperSissor.query.all()
    win = RockPaperSissor.query.filter_by(result="승").count()
    lose = RockPaperSissor.query.filter_by(result="패").count()
    tie = RockPaperSissor.query.filter_by(result="무").count()



    context = {'player':player,
                'computer':computer,
                'result': game_result,
                "win" : win,
                'lose' : lose,
                'tie' : tie,
                'record_list':record_list
                }

    return render_template("game.html", data=context)



if __name__ == '__main__':
    app.run(debug=True)
