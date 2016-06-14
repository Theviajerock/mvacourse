from flask import Flask, render_template, request
import redis

app = Flask(__name__)

r = redis.StrictRedis(host='localhost', port=6379, db=0, charset="utf-8", decode_responses=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/create', methods=['GET','POST'])
def create():
    if request.method == "GET":
        return render_template('create.html')
    elif request.method == "POST":
        title = request.form['title']
        question = request.form['question']
        answer = request.form['answer']
        r.set(title + ':question', question)
        r.set(title + ':answer', answer)
        return render_template('created.html', question=question, answer=answer)

@app.route('/question/<title>', methods=['GET','POST'])
def question(title):
    if request.method == "GET":
        question = r.get(title + ':question')
        return render_template('answerquestion.html', question=question)
    elif request.method == "POST":
        if r.get(title + ':answer') == request.form['answer']:
            question = r.get(title + ':question')
            answer = r.get(title + ':answer')
            return render_template('CorrectAnswer.html', answer = answer, question = question)
        else:
            return 'Incorrect answer'

app.run(debug=True, host="0.0.0.0")
