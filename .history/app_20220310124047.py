from flask import Flask, url_for, redirect, session, render_template
import login

app = Flask(__name__)


@app.route('/')
def index():
    return 'index'

@app.route('/')
def login_page():
    if 'page' in session:
        return f'{session["page"]}'
    return login.handle()


@app.route('/logout')
def logout():
   # remove the username from the session if it is there
   session.pop('username', None)
   return redirect('/')


app.secret_key = 'cattofatto'

if __name__ == '__main__':
    app.run(debug=True)