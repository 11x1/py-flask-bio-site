from flask import Flask, url_for, redirect, session, render_template, request
import mysql.connector

from sql_helpers import login_and_return_db

app = Flask(__name__)
app.secret_key = 'cattofatto'

@app.route('/', methods=['GET'])
def index():
    if 'username' in session: return redirect(f'users/{session["username"]}.{session["uid"]}')
    return redirect('login')


@app.route('/login', methods=['GET', 'POST'])
def login_page():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        db = login_and_return_db()
        db_cursor = db.cursor()
        db_cursor.execute('use webdev')
        #db_cursor.execute(f'select username, password from users where username="{username}" and password="{password}"')
        db_cursor.execute(f'select username, password, userid from users where username="{username}"')
        query = db_cursor.fetchall()
        if len(query) == 0: error = f'User {username} does not exist'
        else:
            db_returned_password = query[0][1]
            if not db_returned_password == password: error = f'Wrong password'
            session['username'] = username
            session['uid'] = query[0][2]
            return redirect('profile')

    return render_template('login.html', error=error)


@app.route('/register', methods=['GET', 'POST'])
def register_page():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        password_repeat = request.form['password_repeat']

        if not password_repeat == password: error = 'passwods do not match'
        elif len(username) < 3: error = 'username is too short'
        elif len(password) < 8: error = 'password is too short'
        else:
            db_cursor = login_and_return_db()
            rows = db_cursor.execute('select * from users')
            db_cursor.execute(f'INSERT INTO users (userid, username, password, profile_picture, description) VALUES ({rows + 1});')
            

    return render_template('register.html', error=error)


@app.route('/profile')
def profile_page():
    if not 'username' in session: return redirect('login')
    return render_template('profile.html', username=session['username'], uid=session['uid'])


@app.route('/logout')
def logout():
   # remove the username from the session if it is there
   session.pop('username', None)
   return redirect('/')


if __name__ == '__main__':
    app.run(debug=True)