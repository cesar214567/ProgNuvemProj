from flask import Flask,render_template, request, session, Response, redirect
from model import entities, db, engine
import producer as tweetg
import filters as filters
import json
import time
import os,sys
from datetime import datetime

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/static/<content>')
def static_content(content):
    return render_template(content)

if __name__ == '__main__':
    app.secret_key  = ".."
    app.run(port=8080, threaded=True, host=('127.0.0.1'))


