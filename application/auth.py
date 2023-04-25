from flask import Blueprint, request, redirect, render_template, flash, url_for, session
from .models import Users
from werkzeug.security import check_password_hash, generate_password_hash
from .extensions import db
from .utils import valid_email


auth = Blueprint("auth", __name__)


# LOGIN ROUTE
@auth.route("/login", methods=["GET", "POST"])
def login():
    # POST
    if request.method == "POST":
        # Clear session
        session.clear()

        username = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")

        # Check for input
        if not username or not email or not password:
            flash("Please provide all inputs!", "error")
            return redirect(url_for("login"))
        elif not valid_email(email):
            flash("Invalid email!", "error")
            return redirect(url_for("login"))
        
        # Check if user exists
        user = Users.query.filter_by(email=email).first()

        # Check if account is activated
        if not user.is_activated:
            flash("Account is not activated, check confirmation link sent to your email to activate!", "error")
            return redirect(url_for("login"))
        
        if not user or not check_password_hash(user.password, password):
            flash("Invalid email or password!", "error")
            return redirect(url_for("login"))

        # Set session var
        session["user_id"] = user.id

        flash("Logged in!", "success")
        return redirect("/")

    # GET
    user = Users.query.filter_by(id=session.get("user_id")).first()
    if user:
        flash("Already logged in!", "error")
        return redirect("/")

    return render_template("login.html")


# LOGOUT ROUTE
@auth.route("/logout")
def logout():
    # Clear session
    session.clear()
    flash("Logged out!", "neutral")

    return redirect("/")


# REGISTER ROUTE
@auth.route("/signup", methods=["GET", "POST"])
def signup():
    # POST
    if request.method == "POST":
        username = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        # Check input
        if not username or not password or not confirmation or not email:
            flash("Please provide all inputs!", "error")
            return redirect(url_for("signup"))
        elif password != confirmation:
            flash("Passwords don't match!", "error")
            return redirect(url_for("signup"))
        elif valid_email(email):
            flash("Invalid email!", "error")
            return redirect(url_for("signup"))

        # Check if user already exists
        user = Users.query.filter_by(email=email).first()

        if user:
            flash("Account already exists!", "error")
            return redirect(url_for("signup"))

        # Create a user
        user = Users(email, username, generate_password_hash(password))

        # Add user to db
        db.session.add(user)
        db.session.commit()

        # Add to session var
        session["user_id"] = user.id

        flash("Account registered!", "success")
        return redirect("/")

    # GET
    user = Users.query.filter_by(id=session.get("user_id")).first()
    if user:
        flash("Already logged in!", "error")
        return redirect("/")

    return render_template("signup.html")


# CHANGE PASSWORD ROUTE
@auth.route("/change-password", methods=["POST"])
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
    user = Users.query.filter_by(id=session.get("user_id")).first()

    if not user:
        flash("Error updating password", "error")
        return redirect("/profile")

    # Update password
    user.password = generate_password_hash(password)
    db.session.commit()

    session.clear()
    flash("Password updated successfully!", "success")
    return redirect("/login")
