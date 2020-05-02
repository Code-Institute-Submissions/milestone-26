from flask import Flask,render_template, request, redirect, url_for
from config import Config
from forms import CreateFilmForm, UpdateFilmForm, ConfirmDelete
from flask_pymongo import PyMongo, DESCENDING
from bson.objectid import ObjectId
import os
import urllib

app = Flask(__name__)
app.config['MONGO_DBNAME']= 'films'
username = urllib.parse.quote_plus('admin1')
password = urllib.parse.quote_plus('movies')
app.config["MONGO_URI"]= "mongodb+srv://admin1:movies@cluster0-xnfne.mongodb.net/films?retryWrites=true&w=majority"
app.config["SECRET_KEY"]= "hweiufhiwuehfuiwegfiwegf"
mongo=PyMongo(app)

@app.route('/')
@app.route('/index')
def index():
    hello="some message"
    films=mongo.db.films.find()
    return render_template("index.html",films=films, message=hello)

@app.route('/create_film', methods=['GET', 'POST'])
def create_film():
    form = CreateFilmForm(request.form)

    if form.validate_on_submit():
        movies = mongo.db.films
        movies.insert_one({
            'title': request.form['title'],
            'description': request.form['description'],
            'director': request.form['director'],
            'image_url': request.form['image_url'],
            'genre': request.form['genre']
        })
        return redirect(url_for('index'))
    return render_template('addfilm.html', form=form)

@app.route('/update_film/<film_id>', methods=['GET', 'POST'])
def update_film(film_id):
    film_db = mongo.db.films.find_one_or_404({'_id': ObjectId(film_id)})

    if request.method == 'GET':
        form = UpdateFilmForm(data=film_db)
        return render_template('updatefilm.html', film=film_db, form=form)
    form = UpdateFilmForm(request.form)
    if form.validate_on_submit():
        films_db = mongo.db.films
        films_db.update_one({
            '_id': ObjectId(film_id),
        }, {
            '$set': {
                'title': request.form['title'],
                'description': request.form['description'],
                'image_url': request.form['image_url'],
                'director': request.form['director'],
                'genre': request.form['genre'],
            }
        })
        return redirect(url_for('index'))
    return render_template('updatefilm.html', film=film_db, form=form)

@app.route('/delete_film/<film_id>', methods=['GET', 'POST'])
def delete_film(film_id):
    film_db = mongo.db.films.find_one_or_404({'_id': ObjectId(film_id)})
    if request.method == 'GET':
        form = ConfirmDelete(data=film_db)
        return render_template('deletefilm.html', title="Delete film", form=form)

    form = ConfirmDelete(request.form)
    if form.validate_on_submit():
        films_db = mongo.db.films
        films_db.delete_one({
            '_id': ObjectId(film_id),
        })
        return redirect(url_for('index'))
    return render_template('deletefilm.html', film=film_db, form=form)

app.run(host=os.getenv("IP", "0.0.0.0"),
        port=int(os.getenv("PORT", "5000")), debug=True)
