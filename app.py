from flask import Flask, render_template, session, redirect
from functools import wraps



app = Flask(__name__)
app.secret_key = 'secret_key'

# DB
import pymongo 
from pymongo import MongoClient
client = pymongo.MongoClient("mongodb+srv://ylee21:0000@cluster0.bnf6h1k.mongodb.net/?retryWrites=true&w=majority")
db = client.login_sys


# Decorators
def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        return f(*args, **kwargs) if 'logged_in' in session else redirect('/')
    return wrap 

# Routes 
from user import routes 
@app.route('/')
def home():
    return render_template("home.html")

@app.route('/dashboard/') # add extra / at the end
@login_required
def dashboard():
    return render_template("dashboard.html")

if __name__ == '__main__':
    app.run(debug=True)
