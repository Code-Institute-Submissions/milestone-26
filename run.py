"""
Simple Flask app, which prints whatever POST data it receives
for API testing purposes.
"""
from flask import Flask,render_template, request
from config import Config
from forms import CreateFilmForm, UpdateFilmForm, ConfirmDelete
from flask_pymongo import PyMongo, DESCENDING
import os
import urllib

app = Flask(__name__)
app.config['MONGO_DBNAME']= 'films'
username = urllib.parse.quote_plus('admin1')
password = urllib.parse.quote_plus('movies')
app.config["MONGO_URI"]= "mongodb+srv://admin1:movies@cluster0-xnfne.mongodb.net/films?retryWrites=true&w=majority"
mongo=PyMongo(app)

@app.route('/')
@app.route('/index')
def index():
    hello="some message"
    films=mongo.db.films.find()
    return render_template("index.html",films=films, message=hello)


app.run(host=os.getenv("IP", "0.0.0.0"),
        port=int(os.getenv("PORT", "5000")), debug=True)
