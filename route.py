from flask import Flask, url_for, render_template, request
import redis


app = Flask(__name__)

#Connection to redis data store
r = redis.StrictRedis(host='localhost', port = 6379, db = 0, charset='utf-8', decode_responses=True)


@app.route('/')
def hello():
    createLink = "<a href='" + url_for('create') + "'> Create a question</a>"
    return """<html>
                    <head>
                        <title> Hello, World </title>
                    </head>
                <body>
                    """ + createLink + """
                </body>
               </html>"""

@app.route('/create', methods=['GET','POST'])
def create():
    if request.method == 'GET':
        return render_template('CreateQuestion.html')
    elif request.method == 'POST':
        #read form data and save it
        title = request.form['title']
        question = request.form['question']
        answer = request.form['answer']
        #store data in data store
        r.set(title + ':question', question)
        r.set(title + ':answer', answer)
        return render_template('CreatedQuestion.html', question = question)
    else:
        return "<h2> Invalid Request</h2>"

@app.route('/question/<title>', methods=['GET','POST'])
def question(title):
    if request.method == 'GET':
        #send the user form
        question = r.get (title + ':question')
        #read question from data store
        return render_template('AnswerQuestion.html', question = question)
    elif request.method == 'POST':
        submittedAnswer = request.form['submittedAnswer']
        #read data from data store
        answer = r.get(title+':answer')
        if submittedAnswer == answer:
            return render_template('Correct.html')
        else:
            return render_template('Incorrect.html', submittedAnswer = submittedAnswer, answer = answer)
    else:
        return '<h2>Invalid Request</h2>'

app.run(debug=True)
