import requests
import os
import urllib.parse


# Parse Reponse to JSON
def parse_response(response):
    try:
        response = response.json()
        return response
    except (TypeError, ValueError, KeyError):
        return None


# Get weekly trending movies
def trending_movies_weekly():

    # Contacting the API
    try:
        apikey = os.getenv("API_KEY")
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
        apikey = os.getenv("API_KEY")
        url = f"https://api.themoviedb.org/3/trending/tv/week?api_key={apikey}"
        response = requests.get(url)
        response.raise_for_status
    except requests.RequestException:
        return None

    # Parse response
    return parse_response(response)


# Get latest movies
def now_playing_movies():

    # Contacting the API
    try:
        apikey = os.getenv("API_KEY")
        url = f"https://api.themoviedb.org/3/movie/now_playing?api_key={apikey}&language=en-US&page=1"
        response = requests.get(url)
        response.raise_for_status
    except requests.RequestException:
        return None

    # Parse response
    return parse_response(response)


# Get latest movies
def on_air_shows():

    # Contacting the API
    try:
        apikey = os.getenv("API_KEY")
        url = f"https://api.themoviedb.org/3/tv/on_the_air?api_key={apikey}&language=en-US&page=1"
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
        apikey = os.getenv("API_KEY")
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
        apikey = os.getenv("API_KEY")
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
        apikey = os.getenv("API_KEY")
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
        apikey = os.getenv("API_KEY")
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
        apikey = os.getenv("API_KEY")
        url = f"https://api.themoviedb.org/3/movie/{id}/similar?api_key={apikey}&language=en-US&include_adult=false"
        response = requests.get(url)
        response.raise_for_status
    except requests.RequestException:
        return None

    # Parse response
    return parse_response(response)


# Get similar shows
def get_similar_shows(id):

    # Contacting the API
    try:
        apikey = os.getenv("API_KEY")
        url = f"https://api.themoviedb.org/3/tv/{id}/similar?api_key={apikey}&language=en-US&page=1"
        response = requests.get(url)
        response.raise_for_status
    except requests.RequestException:
        return None

    # Parse response
    return parse_response(response)


def get_main_posters():

    # Contacting the API
    try:
        apikey = os.getenv("API_KEY")
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


# Get videos related to the movie
def get_movie_video(id):
    try:
        apikey = os.getenv("API_KEY")
        url = f"https://api.themoviedb.org/3/movie/{id}/videos?api_key={apikey}&language=en-US"
        response = requests.get(url)
        response.raise_for_status
    except requests.RequestException:
        return None

    return parse_response(response)


# Get videos related to the show
def get_show_video(id):
    try:
        apikey = os.getenv("API_KEY")
        url = f"https://api.themoviedb.org/3/tv/{id}/videos?api_key={apikey}&language=en-US"
        response = requests.get(url)
        response.raise_for_status
    except requests.RequestException:
        return None

    return parse_response(response)
