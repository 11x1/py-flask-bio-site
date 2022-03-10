import mysql.connector
def login_and_return_db(): 
    db = mysql.connector.connect(
        host='localhost',
        user='root',
        passwd='password'
    )

    return db