from flask import Flask,render_template
from config import Config
from forms import CreateFilmForm, UpdateFilmForm, ConfirmDelete
from flask_pymongo import PyMongo, DESCENDING
import os


app = Flask(__name__)
app.config['MONGO_DBNAME']= 'films'
app.config["MONGO_URI"]= "mongodb+srv://<USERNAME>:<admin>@<cluster>-bs7ct.mongodb.net/<DATABASE>?retryWrites=true"
mongo=PyMongo(app)
@app.route('/')
@app.route('/index')
def index():
    films=mongo.db.films.find()


    return render_template('index.html',films=films)


if __name__ == '__main__':
    app.run()