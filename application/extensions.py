from flask_sqlalchemy import SQLAlchemy
from flask_session import Session
from flask_mail import Mail


# Create objects
db = SQLAlchemy()
session = Session()
mail = Mail()