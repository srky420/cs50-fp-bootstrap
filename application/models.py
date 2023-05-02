from .extensions import db
from datetime import date


# Users
class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), nullable=False, unique=True)
    username = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(200), nullable=False)
    is_activated = db.Column(db.Boolean, nullable=False, default=False)
    reset_token = db.Column(db.String(200), nullable=True, default="")
    movies = db.relationship("Movies", backref="user")
    shows = db.relationship("Shows", backref="user")

    def __init__(self, email, username, password):
        self.email = email
        self.username = username
        self.password = password
        self.is_activated = False


# Movies
class Movies(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    movie_id = db.Column(db.Integer, nullable=False)
    watched = db.Column(db.Boolean, nullable=False, default=False)
    added_on = db.Column(db.Date, default=date.today())
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))

    def __init__(self, movie_id, watched, user_id):
        self.movie_id = movie_id
        self.watched = watched
        self.user_id = user_id


# Movies
class Shows(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    show_id = db.Column(db.Integer, nullable=False)
    watched = db.Column(db.Boolean, nullable=False, default=False)
    added_on = db.Column(db.Date, default=date.today())
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))

    def __init__(self, show_id, watched, user_id):
        self.show_id = show_id
        self.watched = watched
        self.user_id = user_id
