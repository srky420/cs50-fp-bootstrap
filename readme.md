# AMDb 
![](./static/All_Movie_Db.png)

### Browse, Search and Watchlist your favorite Movies and TV Shows    
  
<br>

## Features
#
- Browse new, trending and popular movies and tv shows
- Access details like ratings, overviews, release dates and posters
- Watchlist movies and tv shows in realtime without page reload
- Get similar movie and tv show suggestions
- Access all seasons of tv shows with details of each episode
- Search titles with ease using auto suggestions
- Signup to add titles to your watchlist

<br>

## Requirements
#
- flask
- flask_session 
- flask_sqlalchemy
- werkzeug.security
- requests
- urllib.parse
- functools
- os

<br>

## Installation
#
1. First download and install Python 3 [here](https://www.python.org/downloads/)

    Ensure Python 3 is installed

        python --version

2. Install pip from [here](https://pip.pypa.io/en/stable/installation/) (Note: Make sure to add Python to environment variables)

    Ensure pip is installed

        pip --version

3. Use pip to install Python packages e.g. flask, flask_sqlalchemy and requests

        pip install flask

        pip install flask_sqlalchemy

        pip install requests
        
4. Clone the project from GitHub repo [here]()

        git clone <url>

## Usage
#
1. Be sure to signup at TMDb [here](https://www.themoviedb.org/) and get your free API KEY

2. After receiving your API KEY, make sure to store it in this environment variable as follow

        $env:API_KEY="<API KEY>"

3. Run the app using

        python app.py

<br>

**Note**: API KEY must be set each time you reopen the project



