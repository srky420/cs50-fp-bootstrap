from flask import Flask, render_template, request, redirect, flash, session, jsonify
from flask_session import Session
from flask_sqlalchemy import SQLAlchemy
from helpers import login_required, trending_movies_weekly, trending_shows_weekly, get_movie, get_show, search_query, get_similar_movies, get_similar_shows, get_main_posters, get_season, now_playing_movies, on_air_shows, get_movie_video, get_show_video
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import date


# App config
app = Flask(__name__)
app.secret_key = "vP\x14U\x99\xb7\xa6n\x10\xb5<\x84\xcea\x96\x1dT2\x9f\xdaY\xc95k"

# Session config
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# SQLAlchemy config
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///allmovie.sqlite3"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)


# DATA MODEL
# Users
class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(200), nullable=False)
    movies = db.relationship("Movies", backref="user")

    def __init__(self, username, password):
        self.username = username
        self.password = password
        

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
        

# INDEX ROUTE
@app.route("/")
def index():
    # image format for TMDB: http://image.tmdb.org/t/p/w500/your_poster_path

    # Get trending movies 
    trending_movs = trending_movies_weekly()
    trending_movs = trending_movs["results"]
   

    # Get trending shows
    trending_shows = trending_shows_weekly()
    trending_shows = trending_shows["results"]
    
    # Get now playing movies
    latest_movies = now_playing_movies()
    latest_movies = latest_movies["results"]
    
    # Get on air shows
    shows_on_air = on_air_shows()
    shows_on_air = shows_on_air["results"]
    
    # Remove duplicate movies
    for i in range(len(latest_movies)):
        for j in range(len(trending_movs)):
            if latest_movies[i]["id"] == trending_movs[j]["id"]:
                latest_movies[i].clear()
                break
            
    # Remove duplicate shows
    for i in range(len(shows_on_air)):
        for j in range(len(trending_shows)):
            if shows_on_air[i]["id"] == trending_shows[j]["id"]:
                shows_on_air[i].clear()
                break

    
    # Get username
    user = Users.query.filter_by(id = session.get("user_id")).all()
    username = ""
    added_movies = []
    added_shows = []
    
    # Get already watchlisted content
    if len(user) == 1:
        username = user[0].username
        movies = Movies.query.filter_by(user_id = user[0].id).all()
        for movie in movies:
            added_movies.append(movie.movie_id)
        
        shows = Shows.query.filter_by(user_id = user[0].id).all()
        for show in shows:
            added_shows.append(show.show_id)


    # Get poster of trending movie
    slides = get_main_posters()
    
    return render_template(
        "index.html", trending_movs=trending_movs, trending_shows=trending_shows, username=username, 
        slides=slides, added_movies=added_movies, added_shows=added_shows, latest_movies=latest_movies, shows_on_air=shows_on_air
        )


# MOVIE ROUTE
@app.route("/movie/<int:id>")
def movie(id):
    info = get_movie(id)
    video = get_movie_video(id)
    
    # Get username
    user = Users.query.filter_by(id = session.get("user_id")).all()
    username = ""
    if len(user) == 1:
        username = user[0].username
    
    # Check if movie is watchlisted
    movies = Movies.query.filter_by(user_id = session.get("user_id"), movie_id = id).all()
    is_added = False
    
    # Check if movie already in watchlist
    if len(movies) == 1:
        is_added = True
    
    # Check for exsiting movies in similar movies list
    added = []
    existing_movies = Movies.query.filter_by(user_id = session.get("user_id")).all()
    for movie in existing_movies:
        if movie:
            added.append(movie.movie_id)
    
    # Video results
    trailer = {}
    video = video["results"]
    for vid in video:
        if vid["type"] == "Trailer":
            trailer = vid
            break

    similar_movies = get_similar_movies(id)
    similar_movies = similar_movies["results"]
    return render_template("movie.html", info=info, similar_movies=similar_movies, is_added=is_added, added=added, username=username, trailer=trailer)


# SHOW ROUTE
@app.route("/show/<int:id>")
def show(id):
    info = get_show(id)
    video = get_show_video(id)

     # Get username
    user = Users.query.filter_by(id = session.get("user_id")).all()
    username = ""
    if len(user) == 1:
        username = user[0].username
    
    # Check if show has been added before
    shows = Shows.query.filter_by(user_id = session.get("user_id"), show_id = id).all()
    is_added = False
    
    # Check if its on watchlist
    if len(shows) == 1:
        is_added = True
        
    # Check for exsiting shows in similar shows list
    added = []
    existing_shows = Shows.query.filter_by(user_id = session.get("user_id")).all()
    for show in existing_shows:
        if show:
            added.append(show.show_id)
            
    # Video results
    trailer = {}
    video = video["results"]
    for vid in video:
        if vid["type"] == "Trailer":
            trailer = vid
            break        
    
    # Get similar shows    
    similar_shows = get_similar_shows(id)
    similar_shows = similar_shows["results"]
    return render_template("show.html", info=info, is_added=is_added, username=username, added=added, similar_shows=similar_shows, trailer=trailer)


# SEASON ROUTE
@app.route("/season/<int:id>&<int:num>&<string:title>")
def season(id, num, title):
    # Get username
    user = Users.query.filter_by(id = session.get("user_id")).all()
    username = ""
    if len(user) == 1:
        username = user[0].username
        
    # Get info
    info = get_season(id, num)
    
    return render_template("season.html", info=info, title=title, username=username)


# SEARCH ROUTE
@app.route("/search")
def search():
    
    # Get username
    user = Users.query.filter_by(id = session.get("user_id")).all()
    username = ""
    if len(user) == 1:
        username = user[0].username
    
    title = request.args.get("search")
    page = request.args.get("page")
    response = search_query(title, page)
    return render_template("search.html", response=response, title=title, username=username)


# SEARCH REALTIME
@app.route("/search-rt")
def search_rt():
    
    # Get title
    title = request.args.get("search")
    response = search_query(title, 1)
    response = response["results"]
        
    return jsonify(response)


# LOGIN ROUTE
@app.route("/login", methods=["GET", "POST"])
def login():
    # POST
    if request.method == "POST":
    # Clear session
        session.clear()
        
        username = request.form.get("username")
        password = request.form.get("password")

        # Check for input
        if not username or not password:
            flash("Invalid username or password!", "error")
            return redirect("/login")
        
        # Check if user exists
        user = Users.query.filter_by(username = username).all()
        
        if len(user) != 1 or not check_password_hash(user[0].password, password):
            flash("Invalid username or password!", "error")
            return redirect("/login")
        
        # Set session var
        session["user_id"] = user[0].id
        
        flash("Logged in!", "success")
        return redirect("/")
    
    # GET
    user = Users.query.filter_by(id = session.get("user_id")).all()
    if len(user) == 1:
        flash("Already logged in!", "error")
        return redirect("/")
    
    return render_template("login.html")
    
    
# LOGOUT ROUTE 
@app.route("/logout")
def logout():
    # Clear session
    session.clear()
    flash("Logged out!", "neutral")
    
    return redirect("/")
    
    
# REGISTER ROUTE
@app.route("/signup", methods=["GET", "POST"])
def signup():
    # POST
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")
        
        # Check input
        if not username or not password or not confirmation:
            flash("Invalid username or password!", "error")
            return redirect("/signup")
        elif password != confirmation:
            flash("Passwords don't match!", "error")
            return redirect("/signup")
        
        # Check if username already exists
        users = Users.query.filter_by(username = username).all()
        
        if len(users) != 0:
            flash("Username already exists!", "error")
            return redirect("/signup")
        
        # Create a user
        user = Users(username, generate_password_hash(password))
            
        # Add user to db
        db.session.add(user)
        db.session.commit()
        
        session["user_id"] = user.id
        
        flash("Account registered!", "success")
        return redirect("/")

    # GET
    user = Users.query.filter_by(id = session.get("user_id")).all()
    if len(user) == 1:
        flash("Already logged in!", "error")
        return redirect("/")
    
    return render_template("signup.html")


# CHANGE PASSWORD ROUTE
@app.route("/change-password", methods=["POST"])
def change_password():
    # Get input
    password = request.form.get("password")
    confirmation = request.form.get("confirmation")
    
    # Check input
    if not password or not confirmation:
        flash("Invalid password!", "error")
        return redirect("/profile")
    elif password != confirmation:
        flash("Passwords don't match!", "error")
        return redirect("/profile")
    
    # Get user
    user = Users.query.filter_by(id = session.get("user_id")).all()
    
    if len(user) != 1:
        flash("Error updating password", "error")
        return redirect("/profile")
    
    # Update password
    user[0].password = generate_password_hash(password)
    db.session.commit()
    
    session.clear()
    flash("Password updated successfully!", "success")
    return redirect("/login")


# PROFILE ROUTE
@app.route("/profile")
@login_required
def profile():
    # Get data for profile
    user = Users.query.filter_by(id = session.get("user_id")).all()
    
    username = user[0].username
    
    # Get user's movies
    movies = Movies.query.filter_by(user_id = user[0].id).all()
    movies_list = []
    
     # Get user's shows
    shows = Shows.query.filter_by(user_id = user[0].id).all()
    shows_list = []
    
    # Get each movie using movie_id and append details to movies_list[]
    for movie in movies:
        info = get_movie(movie.movie_id)
        movies_list.append(info)
    
    num_of_movies = len(movies_list)
    
    # Get each show using show_id and append to shows_list[]
    for show in shows:
        info = get_show(show.show_id)
        shows_list.append(info)
        
    num_of_shows = len(shows_list)
        
    return render_template("profile.html", username=username, movies_list=movies_list, num_of_movies=num_of_movies, shows_list=shows_list, num_of_shows=num_of_shows)


# ADD MOVIE ROUTE
@app.route("/add-movie/<int:id>", methods=["POST"])
@login_required
def add_movie(id):
    # Check if movie exists
    _movie = Movies.query.filter_by(movie_id = id, user_id = session.get("user_id")).all()
    
    if len(_movie) == 1:
        flash("Error adding movie", "error")
        return redirect(request.referrer)
    
    # Create movie obj
    movie = Movies(id, False, session.get("user_id"))

    db.session.add(movie)
    db.session.commit()
    
    return jsonify("Movie added")


# REMOVE MOVIE ROUTE
@app.route("/remove-movie/<int:id>", methods=["POST"])
@login_required
def remove_movie(id):
    # Check if movie exists
    _movie = Movies.query.filter_by(movie_id = id, user_id = session.get("user_id")).all()
    
    if len(_movie) == 0:
        flash("Error removing movie", "error")
        return redirect(request.referrer)
    
    # Delete movie
    Movies.query.filter_by(movie_id = id, user_id = session.get("user_id")).delete()
    db.session.commit()
    
    return jsonify('Movie removed')


# ADD SHOW ROUTE
@app.route("/add-show/<int:id>", methods=["POST"])
@login_required
def add_show(id):
    # Check if show exists
    _show = Shows.query.filter_by(show_id = id, user_id = session.get("user_id")).all()
    
    if len(_show) == 1:
        flash("Error removing show", "error")
        return redirect(request.referrer)
    
    # Create show obj
    show = Shows(id, False, session.get("user_id"))

    db.session.add(show)
    db.session.commit()
    
    return jsonify("Show added")


# REMOVE SHOW ROUTE
@app.route("/remove-show/<int:id>", methods=["POST"])
@login_required
def remove_show(id):
    # Check if show exists
    show = Shows.query.filter_by(show_id = id, user_id = session.get("user_id")).all()
    
    if len(show) == 0:
        flash("Error removing show", "error")
        return redirect(request.referrer)
    
    # Delete show
    Shows.query.filter_by(show_id = id, user_id = session.get("user_id")).delete()
    db.session.commit()
        
    return jsonify("Show Removed")


# PRIVACY POLICY ROUTE
@app.route("/privacypolicy")
def privacy_policy():
    return render_template("/privacypolicy.html")


# MAIN
if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)