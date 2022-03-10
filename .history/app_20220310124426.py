from flask import Flask, url_for, redirect, session, render_template
import login
import profile

app = Flask(__name__)

session['page'] = 'login'

@app.route('/')
def index():
    return 'index'

@app.route('/')
def login_page():
    if 'username' in session:
        session['page'] = 'profile'
        return profile.handle()
    if 'page' in session:
        if session['page'] == 'login':
            return login.handle()
        elif session['page'] == 'profile': 
            return profile.handle()



@app.route('/logout')
def logout():
   # remove the username from the session if it is there
   session.pop('username', None)
   return redirect('/')


app.secret_key = 'cattofatto'

if __name__ == '__main__':
    app.run(debug=True)