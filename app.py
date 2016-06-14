from flask import Flask, url_for


app = Flask(__name__)

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

@app.route('/create')
def create():
    return "<h2> Create succesful </h2>"

@app.route('/question/<title>')
def question(title):
	return "<h2>" + title + "</h2>"

app.run(debug=True)