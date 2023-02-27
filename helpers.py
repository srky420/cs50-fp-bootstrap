import requests
import os
import urllib.parse
from functools import wraps
from flask import redirect, session, flash, request


# Login required decorator
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            flash("Login required!", "error")
            return redirect("/login")
        
        return f(*args, **kwargs)
    return decorated_function


# Get weekly trending movies
def trending_movies_weekly():

    # Contacting the API
    try:
        apikey = os.environ.get("API_KEY")
        url = f"https://api.themoviedb.org/3/trending/movie/week?api_key={apikey}"
        response = requests.get(url)
        response.raise_for_status
    except requests.RequestException:
        return None

    # Parse response
    return parse_response(response)


# Get weekly trending shows
def trending_shows_weekly():

    # Contacting the API
    try:
        apikey = os.environ.get("API_KEY")
        url = f"https://api.themoviedb.org/3/trending/tv/week?api_key={apikey}"
        response = requests.get(url)
        response.raise_for_status
    except requests.RequestException:
        return None

    # Parse response
    return parse_response(response)


# Get popular movies
def get_popular_movies():

    # Contacting the API
    try:
        apikey = os.environ.get("API_KEY")
        url = f"https://api.themoviedb.org/3/movie/popular?api_key={apikey}&language=en-US"
        response = requests.get(url)
        response.raise_for_status
    except requests.RequestException:
        return None

    # Parse response
    return parse_response(response)


# Get latest movies
def get_latest_movies():

    # Contacting the API
    try:
        apikey = os.environ.get("API_KEY")
        url = f"https://api.themoviedb.org/3/movie/now_playing?api_key={apikey}&language=en-US&page=1"
        response = requests.get(url)
        response.raise_for_status
    except requests.RequestException:
        return None

    # Parse response
    return parse_response(response)


# Get movie details
def get_movie(id):

    # Contacting the API
    try:
        apikey = os.environ.get("API_KEY")
        url = f"https://api.themoviedb.org/3/movie/{id}?api_key={apikey}&language=en-US"
        response = requests.get(url)
        response.raise_for_status
    except requests.RequestException:
        return None

    # Parse response
    return parse_response(response)


# Get show details
def get_show(id):

    # Contacting the API
    try:
        apikey = os.environ.get("API_KEY")
        url = f"https://api.themoviedb.org/3/tv/{id}?api_key={apikey}&language=en-US"
        response = requests.get(url)
        response.raise_for_status
    except requests.RequestException:
        return None

    # Parse response
    return parse_response(response)


# Get season details
def get_season(id, num):
    
    # Contacting the API
    try:
        apikey = os.environ.get("API_KEY")
        url = f"https://api.themoviedb.org/3/tv/{id}/season/{num}?api_key={apikey}&language=en-US"
        response = requests.get(url)
        response.raise_for_status
    except requests.RequestException:
        return None
    
    # Parse response
    return parse_response(response)


# Get search results
def search_query(title, n):

    # Contacting the API
    try:
        apikey = os.environ.get("API_KEY")
        url = f"https://api.themoviedb.org/3/search/multi?api_key={apikey}&query={urllib.parse.quote_plus(title)}&page={n}&language=en-US&include_adult=false"
        response = requests.get(url)
        response.raise_for_status
    except requests.RequestException:
        return None

    # Parse response
    return parse_response(response)
    
    
# Get similar movies
def get_similar_movies(id):
    
    # Contacting the API
    try:
        apikey = os.environ.get("API_KEY")
        url = f"https://api.themoviedb.org/3/movie/{id}/similar?api_key={apikey}&language=en-US&include_adult=false"
        response = requests.get(url)
        response.raise_for_status
    except requests.RequestException:
        return None

    # Parse response
    return parse_response(response)
    
    
def get_main_posters():
    
    # Contacting the API
    try:
        apikey = os.environ.get("API_KEY")
        url = f"https://api.themoviedb.org/3/movie/top_rated?api_key={apikey}&language=en-US&page=1"
        response = requests.get(url)
        response.raise_for_status
    except requests.RequestException:
        return None

    # Parse response
    response = parse_response(response)
    results = []
    for i in range(10):
        results.append(response["results"][i])
        
    return results
    
    
# Parse Reponse to JSON   
def parse_response(response):
    try:
        response = response.json()
        return response
    except (TypeError, ValueError, KeyError):
        return None