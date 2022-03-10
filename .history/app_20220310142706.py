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
        db_cursor.execute(f'select username, password, userid from users where username="{username}"')
        query = db_cursor.fetchall()
        if len(query) == 0: error = f'User {username} does not exist'
        else:
            db_returned_password = query[0][1]
            if not db_returned_password == password: error = f'Wrong password'
            session['username'] = query[0][0]
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
            db = login_and_return_db()
            db_cursor = db.cursor()
            db_cursor.execute('use webdev')
            db_cursor.execute('select count(*) from users')
            rows = db_cursor.fetchone()[0]
            db_cursor.execute(f'INSERT INTO users VALUES({rows + 1}, "{username}", "{password}", {0}, {0})')
            db.commit()
            return redirect('login')

    return render_template('register.html', error=error)


@app.route('/profile')
def profile_page():
    if not 'username' in session: return redirect('login')
    return render_template('profile.html', username=session['username'], uid=session['uid'])


@app.route('/userlist')
def userlist_page():
    if not 'username' in session: return redirect('login')

    db = login_and_return_db()
    cursor = db.cursor()
    cursor.execute('use webdev')
    cursor.execute('select userid, username from users')
    data = cursor.fetchone()
    user_list = []
    for row in data:
        print(data[row])
        user_list.append(data[row])
    
    print(user_list)
    
    return render_template('userlist.html', len=len(user_list), list=user_list)


@app.route('/logout')
def logout():
   # remove the username from the session if it is there
   session.pop('username', None)
   return redirect('/')


if __name__ == '__main__':
    app.run(debug=True)