#!/usr/bin/python3

"""RESTFUL api for parent login and registrations"""
from datetime import datetime, timedelta
from flask.templating import render_template
from api.v1.views.practitioner import generate_session_id
from models.sessionManager import Session
from models import storage
from flask_bcrypt import Bcrypt
from flask import current_app, jsonify, make_response, request, flash
from models.parent import Parent
from api.v1.views import app_views
import re
from flask import render_template, redirect, url_for
from flask_mail import Mail
from models.parent import Parent
from models import storage
from flask import request, flash
from flask_mail import Message

def send_email(to_email, password, name):
    subject = "Welcome to the IMS System!"
    body = f"Dear {name}, \n\nWelcome to the IMS System! Your login credentials are as follows:\n\nUsername: {to_email}\nPassword: {password}\n\nPlease login and explore the system. If you have any questions, feel free to reach out to us.\n\nThank you!"

    # Use Flask-Mail to send the email
    msg = Message(
        subject, sender="mailtrap@vandi.tech", recipients=[to_email], body=body
    )
    current_app.extensions["mail"].send(msg)
    return True

def send_reset_password_email(to_email, token):
    subject = "Password Reset Request"
    body = (
        f"Copy the following token to reset your password: {token} You have 90 seconds"
    )

    # Use your email sending mechanism, for example, Flask-Mail
    msg = Message(
        subject, sender="mailtrap@vandi.tech", recipients=[to_email], body=body
    )
    current_app.extensions["mail"].send(msg)


# function that searches parent by their phome number
def get_by_phone(email):
    """This function returns a parent whose phone number is provided"""
    parents = storage.all("Parent")
    print("parents", parents)
    for parent in parents.values():
        print("parent", parent)
        if parent.email == email:
            return parent

# print the status
@app_views.route("/status", methods=["GET"], strict_slashes=False)
def status():
    """return the status of the api"""
    return jsonify({"status": "OK"}), 200


# a route to register a parent
@app_views.route("/practitioner/parent/register", methods=["GET", "POST"], strict_slashes=False)
def register_parent():
    if request.method == "GET":
        return render_template("parent.html")

    email = request.form.get("email")
    password = request.form.get("password")
    confirm_password = request.form.get("confirm_password")
    first_name = request.form.get("first_name")
    second_Name = request.form.get("second_Name")
    phone_number = request.form.get("phone_number")
    county = request.form.get("county")

    patterns = {
        "email": r"^[a-zA-Z0-9._%-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,4}$",
        "password": r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$",
    }

    errors = {
        "email": "Invalid email format",
        "password": "Password must be at least 8 characters long and contain at least one uppercase letter, one lowercase letter, one digit, and one special character",
    }

    if not all(
        [
            email,
            password,
            confirm_password,
            first_name,
            second_Name,
        ]
    ):
        flash("Kindly fill in all the fields", category="error")

    # Check if passwords match
    if password != confirm_password:
        flash("Passwords do not match", category="error")
        return redirect(url_for("app_views.register_parent"))

    for field, pattern in patterns.items():
        if not re.match(pattern, locals()[field]):
            flash(errors[field], category="error")
            return redirect(url_for("app_views.register_parent"))
    hashed_password = Bcrypt().generate_password_hash(password).decode("utf-8")
    new_parent = Parent(
        email=email,
        password=hashed_password,
        first_name=first_name,
        second_Name=second_Name,
        phone_number=phone_number,
        county=county,
    )

    if storage.get_by_email("Parent", email):
        flash("Parent already exists", category="error")
        # redirect to the same link
        return redirect(url_for("app_views.register_parent"))
    if send_email(email, password, first_name) == True:
        flash(f"Login credentials sent to {new_parent.email}", category="success")
        new_parent.save()
    else:
        flash("Email not sent. Parent Not saved. Try again", category="error")
    return redirect(url_for("app_views.practitioner_dashboard"))

@app_views.route("/parent/register", methods=["GET", "POST"], strict_slashes=False)
def parent_register():
    if request.method == "GET":
        return render_template("parent.html")

    email = request.form.get("email")
    password = request.form.get("password")
    confirm_password = request.form.get("confirm_password")
    first_name = request.form.get("first_name")
    second_Name = request.form.get("second_Name")
    phone_number = request.form.get("phone_number")
    county = request.form.get("county")

    patterns = {
        "email": r"^[a-zA-Z0-9._%-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,4}$",
        "password": r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$",
    }

    errors = {
        "email": "Invalid email format",
        "password": "Password must be at least 8 characters long and contain at least one uppercase letter, one lowercase letter, one digit, and one special character",
    }

    if not all(
        [
            email,
            password,
            confirm_password,
            first_name,
            second_Name,
        ]
    ):
        flash("Kindly fill in all the fields", category="error")

    # Check if passwords match
    if password != confirm_password:
        flash("Passwords do not match", category="error")
        return redirect(url_for("app_views.parent_register"))

    for field, pattern in patterns.items():
        if not re.match(pattern, locals()[field]):
            flash(errors[field], category="error")
            return redirect(url_for("app_views.register_parent"))
    hashed_password = Bcrypt().generate_password_hash(password).decode("utf-8")
    new_parent = Parent(
        email=email,
        password=hashed_password,
        first_name=first_name,
        second_Name=second_Name,
        phone_number=phone_number,
        county=county,
    )
    new_parent.save()
    flash("Registration successful", category="Success")
    return redirect(url_for("app_views.parent_dashboard"))

@app_views.route("/parent/login", methods=["POST", "GET"], strict_slashes=False)
def login_parent():
    """This function logs in a parent"""
    if request.method == "GET":
        return render_template("login.html")
    
    email = request.form.get("email")
    password = request.form.get("password")

    if not email or not password:
        flash("Email and password are required", category="error")
        return redirect(url_for("app_views.login_parent"))

    if "@" not in email:
        flash("Invalid email", category="error")
        return redirect(url_for("app_views.login_parent"))

    if len(password) < 8:
        flash("Password must be at least 8 characters", category="error")
        return redirect(url_for("app_views.login_parent"))

    parent = storage.get_by_email("Parent", email)
    if not parent:
        flash("you sure you are in the system??? TRY AGAIN!!!", category="error")
        return redirect(url_for("app_views.login_parent"))

    if not Bcrypt().check_password_hash(parent.password, password):
        flash("Incorrect password", category="error")
        return redirect(url_for("app_views.login_parent"))
    # create a uuid4 session id that expires after 10 minutes
    session_id = generate_session_id() 
    new_session = Session(email=email)
    new_session.save()
    s = storage.all("Session")
    for _, value in s.items():
        if value.id != new_session.id and value.email == email:
            storage.delete(value)
            storage.save()
            
    session = storage.get_by_email("Session", email)
    set_cookie = make_response(redirect(url_for("app_views.parent_dashboard")))
    
    set_cookie.set_cookie("Session", session.id)
    
    flash(f"Welcome {parent.first_name}!", category="success")
    return set_cookie

# search parent by phone number. This is for the search button for the practitioner
@app_views.route("/practitioner/search", methods=["GET", "POST"])
def search_parent_form():
    user_id = request.cookies.get("Session")
    session = storage.get("Session", user_id)
    if not session or session.expiration_time < datetime.utcnow():
        flash("Session Ended. Login", category="error")
        return redirect(url_for("app_views.login_practitioner"))   
    session.expiration_time = datetime.utcnow() + timedelta(minutes=1)
    storage.save()
    if request.method == "POST":
        phone_number = request.form.get("phone_number")
        if phone_number == "":
            flash("Kindly fill in the phone number", category="error")
            return render_template("parent_search.html", parent=None)
        parent = storage.get_by_phone("Parent", phone_number)
        print(parent)
        if parent is None:
            flash("No parent with that phone number", category="error")
            return render_template("parent_search.html", parent=None)
        else:
            return render_template("parent_search.html", parent=parent)
    return render_template("parent_search.html", parent=None)


@app_views.route("/parent/dashboard", methods=["GET", "POST"], strict_slashes=False)
def parent_dashboard():
    """This function redirects to the parent dashboard"""
    user_id = request.cookies.get("Session")
    session = storage.get("Session", user_id)
    if not session or session.expiration_time < datetime.utcnow():
        flash("LOGIN TO ACCESS THIS PAGE", category="error")
        return redirect(url_for("app_views.login_parent"))   
    session.expiration_time = datetime.utcnow() + timedelta(minutes=2)
    storage.save()
    parent = storage.get_by_email("Parent", session.email)
    children = parent.children
    return render_template("parent_dashboard.html",children=children)



@app_views.route("practitioner/search/<parent_id>", methods=["GET"], strict_slashes=False)
def parent_children(parent_id):
    """This function returns a parent's children"""
    parent = storage.get("Parent", parent_id)
    children = parent.children
    return render_template("parent_search.html", parent=parent)


