from flask import Blueprint, render_template, redirect, request, jsonify, flash, session
from .extensions import db
from .models import Users, Movies, Shows
from application.api import trending_movies_weekly, trending_shows_weekly, \
    get_movie, get_show, search_query, get_similar_movies, get_similar_shows, \
    get_main_posters, get_season, now_playing_movies, on_air_shows, \
    get_movie_video, get_show_video
from .utils import login_required


views = Blueprint("views", __name__)


# INDEX ROUTE
@views.route("/")
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
    user = Users.query.filter_by(id=session.get("user_id")).first()
    username = ""
    added_movies = []
    added_shows = []

    # Get already watchlisted content
    if user:
        username = user.username
        movies = Movies.query.filter_by(user_id=user.id).all()
        for movie in movies:
            added_movies.append(movie.movie_id)

        shows = Shows.query.filter_by(user_id=user.id).all()
        for show in shows:
            added_shows.append(show.show_id)

    # Get poster of trending movie
    slides = get_main_posters()

    return render_template(
        "index.html", trending_movs=trending_movs, trending_shows=trending_shows, username=username,
        slides=slides, added_movies=added_movies, added_shows=added_shows, latest_movies=latest_movies, shows_on_air=shows_on_air
    )


# MOVIE ROUTE
@views.route("/movie/<int:id>")
def movie(id):
    info = get_movie(id)
    video = get_movie_video(id)

    # Get username
    user = Users.query.filter_by(id=session.get("user_id")).first()
    username = ""
    if user:
        username = user.username

    # Check if movie is watchlisted
    movie = Movies.query.filter_by(
        user_id=session.get("user_id"), movie_id=id).first()
    is_added = False

    # Check if movie already in watchlist
    if movie:
        is_added = True

    # Check for exsiting movies in similar movies list
    added = []
    existing_movies = Movies.query.filter_by(
        user_id=session.get("user_id")).all()
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
@views.route("/show/<int:id>")
def show(id):
    info = get_show(id)
    video = get_show_video(id)

    # Get username
    user = Users.query.filter_by(id=session.get("user_id")).first()
    username = ""
    if user:
        username = user.username

    # Check if show has been added before
    show = Shows.query.filter_by(
        user_id=session.get("user_id"), show_id=id).first()
    is_added = False

    # Check if its on watchlist
    if show:
        is_added = True

    # Check for exsiting shows in similar shows list
    added = []
    existing_shows = Shows.query.filter_by(
        user_id=session.get("user_id")).all()
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
@views.route("/season/<int:id>&<int:num>&<string:title>")
def season(id, num, title):
    # Get username
    user = Users.query.filter_by(id=session.get("user_id")).first()
    username = ""
    if user:
        username = user.username

    # Get info
    info = get_season(id, num)

    return render_template("season.html", info=info, title=title, username=username)


# SEARCH ROUTE
@views.route("/search")
def search():

    # Get username
    user = Users.query.filter_by(id=session.get("user_id")).first()
    username = ""
    if user:
        username = user.username

    title = request.args.get("search")
    page = request.args.get("page")
    response = search_query(title, page)
    return render_template("search.html", response=response, title=title, username=username)


# SEARCH REALTIME
@views.route("/search-rt")
def search_rt():

    # Get title
    title = request.args.get("search")
    response = search_query(title, 1)
    response = response["results"]

    return jsonify(response)


# PROFILE ROUTE
@views.route("/profile")
@login_required
def profile():
    # Get data for profile
    user = Users.query.filter_by(id=session.get("user_id")).first()

    username = user.username

    # Get user's movies
    movies = Movies.query.filter_by(user_id=user.id).all()
    movies_list = []

    # Get user's shows
    shows = Shows.query.filter_by(user_id=user.id).all()
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
@views.route("/add-movie/<int:id>", methods=["POST"])
@login_required
def add_movie(id):
    # Check if movie exists
    _movie = Movies.query.filter_by(
        movie_id=id, user_id=session.get("user_id")).first()

    if _movie:
        flash("Error adding movie", "error")
        return redirect(request.referrer)

    # Create movie obj
    movie = Movies(id, False, session.get("user_id"))

    db.session.add(movie)
    db.session.commit()

    return jsonify("Movie added")


# REMOVE MOVIE ROUTE
@views.route("/remove-movie/<int:id>", methods=["POST"])
@login_required
def remove_movie(id):
    # Check if movie exists
    movie = Movies.query.filter_by(
        movie_id=id, user_id=session.get("user_id")).first()

    if not movie:
        flash("Error removing movie", "error")
        return redirect(request.referrer)

    # Delete movie
    Movies.query.filter_by(
        movie_id=id, user_id=session.get("user_id")).delete()
    db.session.commit()

    return jsonify("Movie removed")


# ADD SHOW ROUTE
@views.route("/add-show/<int:id>", methods=["POST"])
@login_required
def add_show(id):
    # Check if show exists
    _show = Shows.query.filter_by(
        show_id=id, user_id=session.get("user_id")).first()

    if _show:
        flash("Error removing show", "error")
        return redirect(request.referrer)

    # Create show obj
    show = Shows(id, False, session.get("user_id"))

    db.session.add(show)
    db.session.commit()

    return jsonify("Show added")


# REMOVE SHOW ROUTE
@views.route("/remove-show/<int:id>", methods=["POST"])
@login_required
def remove_show(id):
    # Check if show exists
    show = Shows.query.filter_by(
        show_id=id, user_id=session.get("user_id")).first()

    if not show:
        flash("Error removing show", "error")
        return redirect(request.referrer)

    # Delete show
    Shows.query.filter_by(show_id=id, user_id=session.get("user_id")).delete()
    db.session.commit()

    return jsonify("Show Removed")


# PRIVACY POLICY ROUTE
@views.route("/privacypolicy")
def privacy_policy():
    return render_template("/privacypolicy.html")