#app.py
from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os
from random import sample

#Flask：建立網頁應用程式
#render_template：用來載入 .html 檔案
#request：取得使用者傳過來的資料
#redirect：讓頁面重新導向
#SQLAlchemy：Flask 連接資料庫的工具
#os：用來取得目前程式的資料夾路徑

app = Flask(__name__) #啟動網站
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data.db') #設定 Flask 要用哪個資料庫。這裡是 SQLite，檔案叫 data.db，會存在 app.py 同一層
db = SQLAlchemy(app) #建立一個 db 物件來操作資料庫

question_bank = {
    'ask': [
        { 'id': '1', 'type': 'rewrite', 'question': "We had an examination <u>at school</u> yesterday.<br>=>____________________________<br>", 'answer': ["Where did we have an examination yesterday?"] },
        { 'id': '2', 'type': 'rewrite', 'question': "<u>Peter</u> was reading a book.<br>=>____________________________<br>", 'answer': ["Who was reading a book?"] },
        { 'id': '3', 'type': 'rewrite', 'question': "My brother enjoys playing <u>volleyball</u>.<br>=>____________________________<br>", 'answer': ["What does your brother enjoy playing?"] },
        { 'id': '4', 'type': 'fill', 'question': "I got 100 on the quiz.<br>=>______ was your grades on the last quiz?<br>", 'answer': ["How"] },
        { 'id': '5', 'type': 'rewrite', 'question': "I brush my teeth <u>every day</u>.<br>=>____________________________<br>", 'answer': ["How often do you brush your teeth?"] }
    ],
    'special_verb': [
        { 'id': '6', 'type': 'rewrite', 'question': "The price of the cup is 700 dollars.<br>She bought it.<br>=>The cup cost __________________<br>", 'answer': ["her 700 dollars."] },
        { 'id': '7', 'type': 'rewrite', 'question': "He spent three hours taking a nap yesterday.<br>=>It took ____________________________<br>", 'answer': ["him three hours to take a nap yesterday."] },
        { 'id': '8', 'type': 'fill', 'question': "His neighbors had a barbecue together last night.<br>=>He heard his neighbors _______ a barbecue together last night.<br>", 'answer': ["having", "have"] },
        { 'id': '9', 'type': 'fill', 'question': "He didn’t edit the video yesterday.<br>=>He forgot _______ the video yesterday.<br>", 'answer': ["to edit"] },
        { 'id':'10', 'type': 'fill', 'question': "Please remember _____________ (sweep) the floor.<br>", 'answer': ["to sweep"] },
        { 'id':'11', 'type': 'fill', 'question': "Jason has played video games for two hours.<br>His mom asks him to stop ________(play) video games.<br>", 'answer': ["playing"] },
        { 'id':'12', 'type': 'rewrite', 'question': "He paid 200 dollars for his dinner.<br>=>He spent _____________________<br>", 'answer': ["200 dollars on his dinner.", "200 dollars buying his dinner"] }
    ],
    'ving': [
        { 'id':'13', 'type': 'rewrite', 'question': "It’s interesting for my sister to fold tissues.<br>=>____________________________<br>", 'answer': ["Folding tissues is interesting for my sister.", "To Fold tissues is interesting for my sister."] },
        { 'id':'14', 'type': 'choice', 'question': "The game sounds _________.<br>", 'options': ("interesting", "interested"), 'answer': ["interesting"] },
        { 'id':'15', 'type': 'choice', 'question': "She is _______ of homework.<br>", 'options': ("tired", "tiring"), 'answer': ["tired"] },
        { 'id':'18', 'type': 'choice', 'question': "_________  the guitar and _________ the song _____ exciting to me.", 'options': ("Playing, singing, is", "Playing, singing, are", "Play, sing, is", "Play, sing, are"), 'answer': ["Playing, singing, are"]},
        { 'id':'19', 'type': 'rewrite', 'question': "My life goal is <u>to travel</u> around the world.<br>=>____________________________<br>", 'answer': ["My life goal is traveling around the world."]}
    ],
    'compare': [
        { 'id':'16', 'type': 'fill', 'question': "Jay paid 20 dollars for the fees.<br>Nico paid 20 dollars for the fees.<br>=>Jay spent _______________(money) Nico did.<br>", 'answer': ["as much money as"] },
        { 'id':'17', 'type': 'fill', 'question': "Alan completed the marathon within 2 hours.<br>Jessie completed it within 2 hours, too.<br>=>Alan ran _______________(fast) Jessie did.<br>", 'answer': ["as fast as"] },
        { 'id':'20', 'type': 'fill', 'question': "The scissor weighs 250 grams.<br>The lamp also weighs 250 grams.<br>=>The scissor weighs _______________(grams) the lamp does.<br>", 'answer': ["as many grams as"]},
        { 'id':'21', 'type': 'fill', 'question': "Amy is 153 centimeters tall.<br>Elma is 171 centimeters tall.<br>=>Amy is _________________(as…as) Elma.", 'answer': ["not as tall as", "not as short as"]},
        { 'id':'22', 'type': 'fill', 'question': "Brook在圖書館盡可能地保持安靜。<br>Brook keeps _____________________(as…as) in the library.", 'answer': ["as quiet as he can"]}
    ],
    'correlative_word':[
        { 'id':'23', 'type': 'reorder', 'question': "neither / coffee / tea / nor / likes / she<br>", 'answer': ["She likes neither coffee nor tea."]},
        { 'id':'24', 'type': 'reorder', 'question': "don’t / I / like / broccoli / and / either / she / doesn’t<br>", 'answer': ["I don’t like broccoli, and she doesn’t either."]},
        { 'id':'25', 'type': 'reorder', 'question': "neither / can / swim / I / John / and<br>", 'answer': ["John can’t swim, and neither can I.", "I can’t swim, and neither can John."]},
        { 'id':'26', 'type': 'rewrite', 'question': "Alice got 59 on the exam.<br>Ian got 47 on the exam.<br>=>_________________ passed the exam.<br>", 'answer': ["Neither of them", "Neither Alice nor Ian"]},
        { 'id':'27', 'type': 'reorder', 'question': "either / she / in / had / hand / her / necklace<br>", 'answer': ["She had her necklace in either hand."]}
    ]
}
picked_questions = []
picked_num = 5

class Question(db.Model):
    id = db.Column(db.String(1000), primary_key=True)
    numOfcorrect = db.Column(db.Integer, default=0)
    numOfwrong = db.Column(db.Integer, default=0)

@app.route('/')
def index():
    return render_template('start.html')

@app.route('/start', methods=['POST'])
def start():
    global picked_questions
    chosen = request.form.getlist('lesson')
    picked_questions.clear()
    for lesson in chosen:
        picked_questions.extend(question_bank[lesson])
    picked_questions = sample(picked_questions, picked_num)
    Percents = []
    for q in picked_questions:
        Q = Question.query.get(q['id'])
        if Q:
            if Q.numOfcorrect+Q.numOfwrong == 0:
                Percents.append(0.0)
            else:
                Percents.append(Q.numOfcorrect/(Q.numOfcorrect+Q.numOfwrong))
        else:
            new_Q = Question(id=q['id'])
            db.session.add((new_Q))
            db.session.commit()
            Percents.append(0.0)
        questionAndpercent_combined = list(zip(picked_questions, Percents))
    return render_template('quiz.html', combined=questionAndpercent_combined)

@app.route('/result', methods=['POST'])
def result():
    results = []
    score = 0
    for i in range(len(picked_questions)):
        q = picked_questions[i]
        user_ans = request.form.get(q['id']) or "未作答"
        corrects = q['answer'].copy()
        for i in range(len(corrects)):
            corrects[i] = corrects[i].replace(' ', '')
        Q = Question.query.get(q['id'])
        if user_ans.replace(' ', '') in corrects:
            results.append(f"Q{i+1}: {q['question']}✅your ans: {user_ans}")
            score += 100/picked_num
            Q.numOfcorrect += 1
        else:
            results.append(f"Q{i+1}: {q['question']}❌your ans: {user_ans}<br>✅correct: {q['answer'][0]}<br>")
            Q.numOfwrong += 1
        db.session.commit()
    return render_template('result.html', score=score, results=results)



if __name__ == "__main__":
    app.run(debug=True)