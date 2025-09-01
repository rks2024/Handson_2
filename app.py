from flask import Flask, render_template

app = Flask(__name__, template_folder="templates")

@app.route('/', methods=['GET'])
def sayhello():
    return "say hello guys, everyone on the floor"

@app.route('/<s>')
def home(s):
    return render_template('home.html', name=s)
    

app.run(debug=True)


