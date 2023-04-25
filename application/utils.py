from functools import wraps
from flask import redirect, session, flash
import re


# Login required decorator
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            flash("Login required!", "error")
            return redirect("/login")

        return f(*args, **kwargs)
    return decorated_function


# Check for valid email
def valid_email(email):
    regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
    if (re.fullmatch(regex, email)):
        return True
    
    return False