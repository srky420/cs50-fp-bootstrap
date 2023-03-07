# AMDb 
![](./static/All_Movie_Db.png)

### Browse, Search and Watchlist your favorite Movies and TV Shows    
  
<br>

## Features

- Browse new, trending and popular movies and tv shows
- Access details like ratings, overviews, release dates and posters
- Watchlist movies and tv shows in realtime without page reload
- Get similar movie and tv show suggestions
- Access all seasons of tv shows with details of each episode
- Search titles with ease using auto suggestions
- Signup to add titles to your watchlist

<br>

## Requirements

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

<br>

## Usage

1. Be sure to signup at TMDb [here](https://www.themoviedb.org/) and get your free API KEY

2. After receiving your API KEY, make sure to store it in an environment variable as follow

        $env:API_KEY="<API KEY>"

3. Run the app using

        python app.py

<br>

**Note**: API KEY must be set each time you reopen the project

<br>

## Implementation Details

### Configuring Flask App

- Creating templates folder to hold html templates and static folder to hold styling and scripting files

- Configure flask app with the help of flask docs [here](https://flask.palletsprojects.com/en/2.2.x/quickstart/)


### Contacting API

- Retreiving API KEY from environment variable using

        os.environ.get("API_KEY")

- Created an appropriate url for specific requests using TMDb instructions and API KEY
- Requests the url using

        url = f"https://"
        response = requests.get(url)

- Checking for errors using try-except
- Parsing response using json()

        response = response.json()

### Creating Database Model

- DB model is created using Python classes and Flask SQLAlchemy with the help of flask docs [here](https://flask-sqlalchemy.palletsprojects.com/en/3.0.x/)

### Creating Routes

- Routes are created with the help of flask and view is created by render_template function

        # Example route

        from flask import render_template

        @app.route('/hello/<name>')
        def hello(name=None):
        return render_template('hello.html', name=name)

- Templates are located in template folder, each route renders a specific template

### Creating JS Requests

- Realtime requests are made for search suggestions and watchlist add/remove buttons using JavaScript fetch
        
        /* For search suggestions */

        response = await fetch(<url>)
        result = await response.json()

        /* For add/remove buttons */

        var options = {
                method: 'POST',
                headers: {
                        'Content-Type': 
                        'appication/json'       
                }
        };
        fetch(<url>, options)
        .then((res) => res.json())
        .then((data) => console.log(data));
        
**Note**: Above code is just an example, see actual JS file for more details and docs [here](https://developer.mozilla.org/en-US/docs/Web/API/Fetch_API/Using_Fetch)

### Creating User Authentication



        

