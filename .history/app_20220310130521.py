from flask import Flask, url_for, redirect, session, render_template

app = Flask(__name__)
app.secret_key = 'cattofatto'


@app.route('/', methods=['GET'])
def index():
    if not 'username' in session: return redirect('login')
    if 'username' in session and 'uid' in session and not session['username'] is None:
        return redirect(f'users/{session["username"]}.{session["uid"]}')


@app.route('/login', methods=['GET', 'POST'])
def login_page():
    return render_template('login')


@app.route('/register', methods=['GET', 'POST'])
def register_page():
    return render_template('register')


@app.route('/logout')
def logout():
   # remove the username from the session if it is there
   session.pop('username', None)
   return redirect('/')


if __name__ == '__main__':
    app.run(debug=True)