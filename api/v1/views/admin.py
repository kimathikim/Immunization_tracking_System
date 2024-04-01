#!/usr/bin/python3
"""Restful api for registration and login for the health admin"""
from datetime import date, timedelta, datetime
from flask import (
    jsonify,
    request,
    current_app,
    flash,
    url_for,
    render_template,
    redirect,
)
from flask_login import login_user, login_required, logout_user

from models.admin import Admin
from models.vaccine import Vaccine
from models.diseases import Disease
from models.parent import Parent
from flask_bcrypt import Bcrypt
from models import storage
import re
from api.v1.views import app_views
import secrets
from werkzeug.utils import secure_filename
import os





ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app_views.route("/admin/register", methods=["POST", "GET"], strict_slashes=False)
def register_admin():
    if request.method == "GET":
        return render_template("register.html")

    email = request.form.get("email")
    password = request.form.get("password")
    confirm_password = request.form.get("confirm_password")
    first_name = request.form.get("first_name")
    second_Name = request.form.get("second_Name")
    phone_number = request.form.get("phone_number")
    id_No = request.form.get("id_No")
    profile_picture = request.files['profile_picture']

    if profile_picture.filename == '':
        flash('No selected file', category='error')
        return redirect(request.url)

    if not allowed_file(profile_picture.filename):
        flash('Invalid file extension. Only PNG, JPG, JPEG, and GIF files are allowed.', category='error')
        return redirect(request.url)

    UPLOAD_FOLDER = 'api/v1/static/prac_images'
    cwd = os.getcwd()
    parts = cwd.split('/')
    cwd = '/'.join(parts)
    upload_path = os.path.join(cwd, UPLOAD_FOLDER)
    try:
        filename = secure_filename(profile_picture.filename)
        profile_picture.save(os.path.join(upload_path, filename))
        flash('File successfully uploaded', category='success')
    except Exception as e:
        flash('An error occurred while uploading the file', category='error')
        current_app.logger.error(f"Error uploading file: {e}")

    patterns = {
        "email": r"^[a-zA-Z0-9._%-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,4}$",
        "phone_number": r"^\d{10}$",
        "password": r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$",
    }

    errors = {
        "email": "Invalid email format",
        "phone_number": "Invalid phone number format",
        "password": "Password must be at least 8 characters long and contain at least one uppercase letter, one lowercase letter, one digit, and one special character",
    }

    # Check if passwords match
    if password != confirm_password:
        flash("Passwords do not match", category="error")
        return redirect(url_for("app_views.register_admin"))

    # Check each field against its pattern
    for field, pattern in patterns.items():
        if not re.match(pattern, locals()[field]):
            flash(errors[field], category="error")
            return redirect(url_for("app_views.register_admin"))

    hashed_password = Bcrypt().generate_password_hash(password).decode("utf-8")

    new_admin= Admin(
        email=email,
        password=hashed_password,
        first_name=first_name,
        second_Name=second_Name,
        profile_picture=profile_picture.filename,
        phone_number=phone_number,
        id_No=id_No,
    )
    # check if the admin exist using the email else save the admin

    if storage.get_by_email("Admin", email):
        flash("Admin already exists", category="error")
        return redirect(url_for("app_views.register_admin"))
    else:
        new_admin.save()
        return redirect(url_for("app_views.admin_dashboard"))



@app_views.route("/admin/login", methods=["POST", "GET"], strict_slashes=False)
def login_admin():
    """This function logs in a admin"""
    if request.method == "GET":
        return render_template("login.html")

    email = request.form.get("email")
    password = request.form.get("password")

    if not email or not password:
        flash("Email and password are required", category="error")
        return redirect(url_for("app_views.login_admin"))

    if "@" not in email:
        flash("Invalid email", category="error")
        return redirect(url_for("app_views.login_admin"))

    if len(password) < 8:
        flash("Password must be at least 8 characters", category="error")
        return redirect(url_for("app_views.login_admin"))

    admin = storage.get_by_email("Admin", email)
    print(admin)
    if not admin:
        flash("No admin with that email", category="error")
        return redirect(url_for("app_views.login_admin"))

    if not Bcrypt().check_password_hash(admin.password, password):
        flash("Incorrect password", category="error")
        return redirect(url_for("app_views.login_admin"))

    # Redirect to the appropriate dashboard route based on the user role
    flash(f"Welcome {admin.first_name}!", category="success")
    return redirect(url_for("app_views.admin_dashboard"))

@app_views.route('/admin/dashboard', methods=['POST', 'GET'], strict_slashes=False)
def admin_dashboard():
    """This function redirects to the admin dashboard"""
    return render_template('admin_dashboard.html')

# create vaccine with all it deGtails
@app_views.route('/admin/vaccine', methods=["POST", "GET"], strict_slashes=False)
def add_vaccine():
    """This function creates a new object for the vaccine model"""
    if request.method == "GET":
        return render_template("vaccine.html")

    vaccine_name = request.form.get("names")
    diseases = request.form.getlist('disease[]')
    no_doses = request.form.get('no_doses')
    descriptions = request.form.getlist("disease_description[]")
    
    if int(no_doses) <= 0 or int(no_doses) > 10:
            flash("Doses must be greater than 0 and less than 10", category="error")
            return redirect(url_for("app_views.add_vaccine"))

    for disease, description in zip(diseases, descriptions):
        if not disease or not description:
            flash("Please fill in all the values", category="error")
            return redirect(url_for("app_views.add_vaccine"))
    print(vaccine_name, diseases, no_doses, descriptions)
    
    # save the vaccine and retrieve the id
    new_vaccine = Vaccine(
        names=vaccine_name,
        no_doses=no_doses,
    )
    new_vaccine.save()
    
    # get the id of the vaccine
    for disease, description in zip(diseases, descriptions):
        new_disease = Disease(
            disease=disease,
            disease_description=description,
            vaccine_id=new_vaccine.id
        )
        new_disease.save()
    
    flash("{{new_vaccine.names}} vaccine added successfully", category="success")
    
    return redirect(url_for("app_views.admin_dashboard"))