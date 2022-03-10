import mysql.connector
def loginand_return_db(): 
    db = mysql.connector.connect(
        host='localhost',
        user='root',
        passwd='password'
    )

    return db