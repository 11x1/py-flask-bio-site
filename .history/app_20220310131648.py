from flask import Flask, url_for, redirect, session, render_template
from flask_sqlalchemy import SQLAlchemy, create_engine
import requests
from sqlalchemy_utils import database_exists, create_database

engine = create_engine("postgres://localhost/mydb")
if not database_exists(engine.url):
    create_database(engine.url)

app = Flask(__name__)
app.secret_key = 'cattofatto'

db_url = 'sqlite:///:memory:'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = db_url
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)

@app.route('/', methods=['GET'])
def index():
    if 'username' in session: return redirect(f'users/{session["username"]}.{session["uid"]}')
    return redirect('login')


@app.route('/login', methods=['GET', 'POST'])
def login_page():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['username']
    return render_template('login.html')


@app.route('/register', methods=['GET', 'POST'])
def register_page():
    return render_template('register.html')


@app.route('/logout')
def logout():
   # remove the username from the session if it is there
   session.pop('username', None)
   return redirect('/')


if __name__ == '__main__':
    app.run(debug=True)