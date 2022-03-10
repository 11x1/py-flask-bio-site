from flask import Flask, url_for, redirect, session, render_template
import login
import profile

app = Flask(__name__)
app.secret_key = 'cattofatto'

session['page'] = 'login'

@app.route('/')
def index():
    return 'index'

@app.route('/', methods=['GET', 'POST'])
def login_page():
    if 'username' in session and session['username'] != None:
        if request.method == 'GET':
            session['page'] = 'profile'
    if 'page' in session:
        if request.method == 'GET':
            if session['page'] == 'login':
                return login.handle()
            elif session['page'] == 'profile': 
                return profile.handle()


@app.route('/logout')
def logout():
   # remove the username from the session if it is there
   session.pop('username', None)
   return redirect('/')


if __name__ == '__main__':
    app.run(debug=True)