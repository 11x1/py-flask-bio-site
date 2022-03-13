import os
from flask import Flask, url_for, redirect, session, render_template, request
from sql_helpers import login_and_return_db, initialize_database
import datetime
import requests
import json
import shutil

# TODO: userid is not row_num + 1, find next free uid from database -> profit $$$

app = Flask(__name__)
app.secret_key = 'cattofatto'

UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'png'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
# Max upload to 16MB
app.config['MAX_CONTENT_LENGTH'] = 16 * 1000 * 1000
app.config['REMEMBER_COOKIE_DURATION'] = datetime.timedelta(seconds=86400)

initialize_database()
db = login_and_return_db()
db_cursor = db.cursor(buffered=True)
db_cursor.execute(f'use webdev')

# https://flask.palletsprojects.com/en/2.0.x/patterns/fileuploads/ 
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/uploads/<filename>')
def render_image(filename):
    if not 'username' in session: return redirect('login')
    return redirect(url_for('static', filename='uploads/' + filename), code=301)


@app.route('/', methods=['GET'])
def index():
    # If we already have logged in in our session, redirect to our profile
    if 'username' in session: return redirect(f'users/{session["username"]}.{session["uid"]}')
    return redirect('login')

@app.route('/login', methods=['GET', 'POST'])
def login_page():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        global db_cursor
        db_cursor.execute(f'select username, password, userid from users where username="{username}"')
        query = db_cursor.fetchall()
        if len(query) == 0: error = f'User {username} does not exist'
        else:
            # query -> [0: username, 1: password, 2: userid] (as selected from database)
            # using query[0][x] to get the first table value
            db_returned_password = query[0][1]
            if db_returned_password != password: error = f'Wrong password'
            else:
                # Set our session values
                session['username'] = query[0][0]
                session['uid'] = query[0][2]
                return redirect(f'users/{session["username"]}.{session["uid"]}')

    return render_template('login.html', error=error)


@app.route('/register', methods=['GET', 'POST'])
def register_page():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        password_repeat = request.form['password_repeat']

        global db_cursor
        db_cursor.execute(f'select username from users where username="{username}"')
        usernames = db_cursor.fetchone()
        if usernames is None:
            if not password_repeat == password: error = 'passwods do not match'
            elif len(username) < 3: error = 'username is too short'
            elif len(password) < 8: error = 'password is too short'
            else:
                global db
                # Select all uids from database
                db_cursor.execute(f'select userid from users')
                data = db_cursor.fetchall()
                uids = []
                # Append each uuid to a list
                for value in data:
                    uids.append(int(value[0]))

                # Simple check if we even have any accounts
                if len(uids) > 0:
                    # If i (integer 1-#uid) is not in uids list, use i as uid
                    for i in range(1, len(uids) + 2):
                        if not i in uids:
                            available_userid = i
                            break
                else:
                    available_userid = 1
                
                # Random dog image from dog.ceo api (cool feature)
                image_url = json.loads(requests.get('https://dog.ceo/api/breeds/image/random').text)['message']
                # Get image bytes
                res = requests.get(image_url)
                # And save the profile picture
                with open(f'static/uploads/{username}.png', 'wb') as f:
                    f.write(res.content)

                # Save our user values to database
                db_cursor.execute(f'INSERT INTO users VALUES({available_userid}, "{username}", "{password}", "{username + ".png"}", "{"Hi my name is " + username}")')
                # Don't forget to commit the changes
                db.commit()
                # Debug message
                print(f'Registered user {username} with uid {available_userid}')
                return redirect('login')
        else: error='username already exists'
    return render_template('register.html', error=error)


@app.route('/userlist', methods=['GET', 'POST'])
def userlist_page():
    # If we aren't logged in, return to login page
    if not 'username' in session: return redirect('login')
    
    is_admin = False
    if session['username'] == 'admin': is_admin = True
    
    global db_cursor

    if request.method == 'POST':
        username = request.form['delete']
        db_cursor.execute(f'delete from users where username="{username}"')
        db.commit()
        os.remove(os.path.join(os.getcwd(), f'static\\uploads\\{username}.png'))

    db_cursor.execute('select userid, username from users')
    data = db_cursor.fetchall()
    user_list = []
    for row in data:
        # row [0: userid, 1: username]
        user_list.append((row[0], row[1], not row[1]=='admin'))
    
    # Sort our values from database to make them look arranged on userlist page
    sorter = lambda x: (x[0], x[1])
    user_list = sorted(user_list, key=sorter)

    return render_template('userlist.html', len=len(user_list), list=user_list, username=session['username'], is_admin=is_admin)


@app.route('/users/<string:username>.<int:userid>', methods=['GET'])
def profile(username, userid):
    # If we aren't logged in, return to login page
    if not 'username' in session: return redirect('../login')

    # check if userid exists
    global db_cursor
    db_cursor.execute(f'select username from users where userid = "{userid}"')
    try:
        real_username = db_cursor.fetchone()[0]
    except:
        return redirect('../profile_not_found')
    
    # Redirect if uid doesnt match username
    if real_username != username: return redirect(f'../users/{real_username}.{userid}')

    # variables if user is the owner of the profile
    is_owner = None

    # Handle if user is owner of the profile
    if session['username'] == username: 
        is_owner = True
        # Edit profile href value
    url = f'users/{session["username"]}.{session["uid"]}'
    
    # Get description and profile picture url from database
    db_cursor.execute(f'select description from users where username = "{username}"')
    profile_description = db_cursor.fetchone()[0]
    db_cursor.execute(f'select profile_picture from users where username="{username}"')
    profile_picture_url = db_cursor.fetchone()[0]
    profile_picture_url = f'static/uploads/{profile_picture_url}'
    print(profile_picture_url)

    # Render profile template with our variables
    #
    # username -> use to show who we are logged in as
    # uid      -> use to show our current user uid
    # 
    # profile_username    -> user profile name we are looking at
    # profile_userid      -> user profile uid we are looking at
    # profile_description -> user profile desc. we are looking at
    # profile_picture_url -> user profile pfp url we are looking at
    # 
    # is_owner -> True if we are looking at our profile
    # url      -> href of 'edit profile' element
    return render_template('profile.html', username=session['username'], uid=session['uid'], profile_username=username, profile_userid=userid, profile_description=profile_description, profile_picture_url=profile_picture_url, is_owner=is_owner, url=url)


@app.route('/profile_not_found')
def profilenofound_page():
    if not 'username' in session: return redirect('login')
    return render_template('profilenotfound.html')


@app.route('/users/<string:username>.<int:userid>/edit', methods=['GET', 'POST'])
def edit_profile(username, userid):
    if not 'username' in session: return redirect('login')
    # if we arent logged in as the user we are looking at, return to user profile page
    if not session['username'] == username: return redirect(f'../users/{username}.{userid}')
    error = None

    global db
    global db_cursor
    
    db_cursor.execute(f'select description from users where username="{username}"')
    description = db_cursor.fetchone()[0]
    db_cursor.execute(f'select profile_picture from users where username="{username}"')
    profile_picture_url = db_cursor.fetchone()[0]

    if request.method == 'POST':
        # get form values
        new_desc = request.form['description']

        #try: 
        file = request.files['profile_picture']
        filename = None
        print(file.filename)
        if file.filename != '' and allowed_file(file.filename):
            filename = f'khey.{str(file.filename)[-3:]}'
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        #except: file = None

        if len(new_desc) > 300: error = 'Description too long (>300 chars)'
        else:
            if new_desc != description:
                db_cursor.execute(f"UPDATE users SET description = '{new_desc}' WHERE username = '{username}'")
        if file is not None and filename is not None and error is None:
            print(filename, profile_picture_url)
            if filename != profile_picture_url:
                db_cursor.execute(f"UPDATE users SET profile_picture = '{filename}' WHERE username = '{username}'")    
        db.commit()
        return redirect(f'/users/{username}.{userid}')
    url = f'../users/{session["username"]}.{session["uid"]}'

    # Render profileedit template with our variables
    #
    # username -> use to show who we are logged in as
    # uid      -> use to show our current user uid
    # 
    # profile_username    -> user profile name we are looking at
    # profile_userid      -> user profile uid we are looking at
    # profile_description -> user profile desc. we are looking at
    # profile_picture_url -> user profile pfp url we are looking at
    # error               -> feedback to user (description too long)
    return render_template('profileedit.html', url=url, username=session['username'], uid=session['uid'], profile_username=session['username'], profile_userid=session['uid'], description=description, profile_picture_url=profile_picture_url, error=error)


@app.route('/logout')
def logout():
   # Remove the username from the session if it is there
   session.pop('username', None)
   session.pop('uid', None)
   return redirect('/')


if __name__ == '__main__':
    app.run(debug=True)