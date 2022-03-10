from flask import Flask, url_for, redirect, session, render_template
import login

app = Flask(__name__)


@app.route('/')
def index():
    return 'index'

@app.route('/login')


app.secret_key = 'cattofatto'

if __name__ == '__main__':
    app.run(debug=True)