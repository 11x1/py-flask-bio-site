from flask import Flask, url_for, redirect, session, render_template
import login
import profile

app = Flask(__name__)
app.secret_key = 'cattofatto'


@app.route('/', methods=['GET', 'POST'])
def login_page():
    return render_template('login.html')


@app.route('/logout')
def logout():
   # remove the username from the session if it is there
   session.pop('username', None)
   return redirect('/')


if __name__ == '__main__':
    app.run(debug=True)