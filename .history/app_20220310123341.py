from flask import Flask, url_for, redirect, session, render_template

app = Flask(__name__)


@app.route('/')
def index():
    return 'index'