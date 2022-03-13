import mysql.connector

def initialize_database():
    db = mysql.connector.connect(
        host='localhost',
        user='root',
        passwd='password'
    )

    cursor = db.cursor()
    cursor.execute('create database if not exists webdev')
    cursor.execute('use webdev')
    cursor.execute('create table if not exists users (userid VARCHAR(255), username VARCHAR(255), password VARCHAR(255), profile_picture VARCHAR(100), description VARCHAR(300))')
    

def login_and_return_db(): 
    db = mysql.connector.connect(
        host='localhost',
        user='root',
        passwd='password'
    )

    return db