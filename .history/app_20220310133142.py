from flask import Flask, url_for, redirect, session, render_template, request
import mysql.connector

from sql_helpers import login_and_return_cursor

app = Flask(__name__)
app.secret_key = 'cattofatto'

@app.route('/', methods=['GET'])
def index():
    if 'username' in session: return redirect(f'users/{session["username"]}.{session["uid"]}')
    return redirect('login')


@app.route('/login', methods=['GET', 'POST'])
def login_page():
    error = None
    

    return render_template('login.html', error=error)


@app.route('/register', methods=['GET', 'POST'])
def register_page():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['username']
        password_repeat = request.form['password_repeat']

        if not password_repeat == password: error = 'passwods do not match'
        else:
            db_cursor = login_and_return_cursor()
            db_cursor.execute('insert into users ')
            

    return render_template('register.html')


@app.route('/logout')
def logout():
   # remove the username from the session if it is there
   session.pop('username', None)
   return redirect('/')


if __name__ == '__main__':
    app.run(debug=True)