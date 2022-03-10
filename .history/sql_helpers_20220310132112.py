import mysql.connector
def login_and_return_cursor(): 
    db = mysql.connector.connect(
        host='localhost',
        user='root',
        passwd='password'
    )

    cursor = db.cursor()
    cursor.execute('use webdev')
    return cursor