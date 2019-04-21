#__author__ == "Priyanka Shanmugasundaram (pshanmu)"
# note: most of this code is modified from lecture

import os
from flask import Flask, render_template, session, redirect, url_for # tools that will make it easier to build on things
from flask_sqlalchemy import SQLAlchemy # handles database stuff for us - need to pip install flask_sqlalchemy in your virtual env, environment, etc to use this and run this

# Application configurations
app = Flask(__name__)
app.debug = True
app.use_reloader = True
app.config['SECRET_KEY'] = '05201996'

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///./college_majors.db' # TODO: decide what your new database name will be -- that has to go here
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


# Set up Flask debug stuff
db = SQLAlchemy(app) # For database use
session = db.session # to make queries easy





#########
######### Everything above this line is important/useful setup, not problem-solving.
#########


##### Set up Models #####

class Major(db.Model):
    __tablename__ = "majors"
    majorcode = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    majorcategory = db.relationship('Major Category',backref='Major')
    recentunemployment = db.Column(db.Float)
    allunemployment = db.Column(db.Float)


class MajorCategory(db.Model):
    __tablename__ = "major category"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    majors = db.relationship('Major',backref='MajorCategory')


##### Helper functions #####

### For database additions
### Relying on global session variable above existing

# to come soon. 


##### Set up Controllers (route functions) #####

# adapted from movies, will add soon. 

## Main route
@app.route('/')
def index():
    movies = Movie.query.all()
    num_movies = len(movies)
    return render_template('index.html', num_movies=num_movies)

@app.route('/movie/new/<title>/<director>/<genre>/')
def new_movie(title, director, genre):
    if Movie.query.filter_by(title=title).first(): # if there is a song by that title
        return "That song already exists! Go back to the main app!"
    else:
        director = get_or_create_director(director)
        movie = Movie(title=title, director_id=director.id,genre=genre)
        session.add(movie)
        session.commit()
        return "New movie: {} by {}. Check out the URL for ALL movies to see the whole list.".format(movie.title, director.name)

@app.route('/all_movies')
def see_all():
    all_movies = [] # Will be be tuple list of title, genre
    movies = Movie.query.all()
    for m in movies:
        director = Director.query.filter_by(id=m.director_id).first() # get just one artist instance
        all_songs.append((m.title,director.name, m.genre)) # get list of songs with info to easily access [not the only way to do this]
    return render_template('all_movies.html',all_movies=all_movies) # check out template to see what it's doing with what we're sending!

@app.route('/all_directors')
def see_all_directors():
    directors = Director.query.all()
    names = []
    for d in directors:
        num_movies = len(Movie.query.filter_by(director_id=d.id).all())
        newtup = (d.name,num_movies)
        names.append(newtup) # names will be a list of tuples
    return render_template('all_directors.html',director_names=names)


if __name__ == '__main__':
    db.create_all() # This will create database in current directory, as set up, if it doesn't exist, but won't overwrite if you restart - so no worries about that
    app.run() # run with this: python main_app.py runserver
