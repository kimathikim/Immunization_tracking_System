#!/usr/bin/python3
"""Restful api for registration and login for the health practitioner"""
import uuid
from flask import (
    jsonify,
    make_response,
    request,
    current_app,
    flash,
    url_for,
    render_template,
    redirect,
)
from flask_bcrypt import Bcrypt
from models import storage
from flask_mail import Message
from models.child import Child
from api.v1.views import app_views
from models.healthcare_provider import Practitioner
from models.sessionManager import Session
from models.parent import Parent
from models.vaccineAdministration import Vaccine_administration
import re
from email.mime.text import MIMEText
import secrets
from datetime import datetime, timedelta
from models import storage
from models.sessionManager import Session
from datetime import datetime, timedelta
from models.dueDate import Duedate
from datetime import datetime, timedelta
import os
import secrets
from werkzeug.utils import secure_filename

app_config = "kimathi"

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def generate_session_id():
    """generate_session_id"""
    id = uuid.uuid4()
    expiration_time = datetime.utcnow() + timedelta(minutes=10)
    return f'{id}_{expiration_time}'
    
def send_email(to_email, password):
    subject = "Welcome to the IMS System!"
    body = f"Dear New Practitioner, \n\nWelcome to the IMS System! Your login credentials are as follows:\n\nUsername: {to_email}\nPassword: {password}\n\nPlease login and explore the system. If you have any questions, feel free to reach out to us.\n\nThank you!"

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
    msg = Message(
        subject, sender="mailtrap@vandi.tech", recipients=[to_email], body=body
    )
    current_app.extensions["mail"].send(msg)


def verify_reset_password(reset_token, new_password):
    """This function verifies that the token has not expired and resets the password"""
    practitioner = storage.get_by_token("Practitioner", reset_token)
    if not practitioner:
        return False
    if practitioner.token_expiration < datetime.now():
        return False
    if new_password is not None:
        hashed_password = Bcrypt().generate_password_hash(new_password).decode("utf-8")
        practitioner.password = hashed_password
        practitioner.save()
        return True


# a route to register a practitioner
@app_views.route(
    "/practitioner/register", methods=["POST", "GET"], strict_slashes=False
)
def register_practitioner():
    if request.method == "GET":
        return render_template("adminRegPrac.html")

    email = request.form.get("email")
    password = request.form.get("password")
    confirm_password = request.form.get("confirm_password")
    first_name = request.form.get("first_name")
    second_Name = request.form.get("second_Name")

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
        return redirect(url_for("app_views.register_practitioner"))

    for field, pattern in patterns.items():
        if not re.match(pattern, locals()[field]):
            flash(errors[field], category="error")
            return redirect(url_for("app_views.register_practitioner"))
    hashed_password = Bcrypt().generate_password_hash(password).decode("utf-8")
    new_practitioner = Practitioner(
        email=email,
        password=hashed_password,
        first_name=first_name,
        second_Name=second_Name,
    )

    if storage.get_by_email("Practitioner", email):
        flash("Practitioner already exists", category="error")
        # redirect to the same link
        return redirect(url_for("app_views.register_practitioner"))
    if send_email(email, password) == True:
        flash(f"Login credentials sent to {new_practitioner.email}", category="success")
        new_practitioner.save()
    return redirect(url_for("app_views.admin_dashboard"))
 

@app_views.route("/practitioner/login", methods=["POST", "GET"], strict_slashes=False)
def login_practitioner():
    """This function logs in a practitioner"""
    if request.method == "GET":
        return render_template("login.html")
    
    email = request.form.get("email")
    password = request.form.get("password")

    if not email or not password:
        flash("Email and password are required", category="error")
        return redirect(url_for("app_views.login_practitioner"))

    if "@" not in email:
        flash("Invalid email", category="error")
        return redirect(url_for("app_views.login_practitioner"))

    if len(password) < 8:
        flash("Password must be at least 8 characters", category="error")
        return redirect(url_for("app_views.login_practitioner"))

    practitioner = storage.get_by_email("Practitioner", email)
    if not practitioner:
        flash("No practitioner with that email", category="error")
        return redirect(url_for("app_views.login_practitioner"))

    if not Bcrypt().check_password_hash(practitioner.password, password):
        flash("Incorrect password", category="error")
        return redirect(url_for("app_views.login_practitioner"))
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
    set_cookie = make_response(redirect(url_for("app_views.practitioner_dashboard")))
    
    set_cookie.set_cookie("Session", session.id)
    
    flash(f"Welcome {practitioner.first_name}!", category="success")
    return set_cookie

# logout route
@app_views.route("/practitioner/logout", methods=["GET"], strict_slashes=False)
def logout_practitioner():
    """This function logs out a practitioner"""
    return redirect(url_for("app_views.login_practitioner"))


@app_views.route("/practitioner/dashboard", methods=["GET", "POST"], strict_slashes=False)
def practitioner_dashboard():
    """This function redirects to the practitioner dashboard"""
    user_id = request.cookies.get("Session")
    session = storage.get("Session", user_id)
    practitioner = storage.get_by_email("Practitioner", session.email)
    if not session or session.expiration_time < datetime.utcnow():
        flash("LOGIN TO ACCESS THIS PAGE", category="error")
        return redirect(url_for("app_views.login_practitioner"))   
    session.expiration_time = datetime.utcnow() + timedelta(minutes=2)
    storage.save()
    print(practitioner)
    return render_template("dashboard.html", practitioner=practitioner)

@app_views.route("/practitioner/dis_images/<filename>", methods=["GET", "POST"], strict_slashes=False)
def display_images(filename):
    print(filename)
    return redirect(url_for("static", filename=f"prac_images/{filename}"), code=301)

@app_views.route("/practitioner/update_profile", methods=["GET", "POST"], strict_slashes=False)
def update_profile():
    """This method updates the profile of the practitioner """
    user_id = request.cookies.get("Session")
    session = storage.get("Session", user_id)
    print(session)
    if not session or session.expiration_time < datetime.utcnow():
        flash("TIMEOUT", category="error")
        return redirect(url_for("app_views.login_practitioner"))   
    session.expiration_time = datetime.utcnow() + timedelta(minutes=30)
    storage.save()
    practitioner = storage.get_by_email("Practitioner", session.email)
    print(practitioner)
    if request.method == "GET":
        return render_template("update_prac.html", practitioner=practitioner)
    
    password = request.form.get("password")
    confirm_password = request.form.get("confirm_password")
    phone_number = request.form.get("phone_number")
    id_No = request.form.get("id_no")
    profile_picture = request.files['profile_picture']
    print(profile_picture)

    if profile_picture.filename == '':
        flash('No selected file', category='error')
        return redirect(request.url)

    if not allowed_file(profile_picture.filename):
        flash('Invalid file extension. Only PNG, JPG, JPEG, and GIF files are allowed.', category='error')
        return redirect(request.url)

    UPLOAD_FOLDER = 'api/v1/static/prac_images'
    cwd = os.getcwd()
    parts = cwd.split('/')
    cwd = '/'.join(parts[:-1])
    upload_path = os.path.join(cwd, UPLOAD_FOLDER)
    try:
        filename = secure_filename(profile_picture.filename)
        profile_picture.save(os.path.join(upload_path, filename))
        flash('File successfully uploaded', category='success')
    except Exception as e:
        flash('An error occurred while uploading the file', category='error')
        current_app.logger.error(f"Errror uploading file: {e}")

    patterns = {
        "phone_number": r"^\d{10}$",
        "id_No": r"^\d{8}$", 
        "password": r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$",
    }

    errors = {
        "phone_number": "Invalid phone number format",
        "id_No": "Invalid Licence number format",
        "password": "Password must be at least 8 characters long and contain at least one uppercase letter, one lowercase letter, one digit, and one special character",
    }
    if password != confirm_password:
        flash("Passwords do not match", category="error")
        return redirect(url_for("app_views.update_profile"))
    
    for field, pattern in patterns.items():
        if not re.match(pattern, locals()[field]):
            flash(errors[field], category="error")
            return redirect(url_for("app_views.update_profile"))

    hashed_password = Bcrypt().generate_password_hash(password).decode("utf-8")

    if not all([phone_number, password, confirm_password, profile_picture]):
        flash("Kindly fill in all the fields", category="error")
        return redirect(url_for("app_views.update_profile"))
    practitioner.phone_number = phone_number
    practitioner.password = hashed_password
    practitioner.profile_picture = profile_picture.filename
    practitioner.id_No = id_No
    practitioner.save()
    flash("Profile updated successfully", category="success")
    return redirect(url_for("app_views.practitioner_dashboard"))


@app_views.route(
    "/practitioner/reset_password", methods=["GET", "POST"], strict_slashes=False
)
def reset_password_link():
    if request.method == "GET":
        
        return render_template("forget_pass.html")

    email = request.form.get("email")

    if not email:
        flash("Email is required", category="error")
        return redirect(url_for("app_views.reset_password_link"))

    practitioner = storage.get_by_email("Practitioner", email)

    if not practitioner:
        flash("No practitioner with that email", category="error")
        return redirect(url_for("app_views.reset_password_link"))

    reset_token = secrets.token_urlsafe(20)
    expiration = datetime.now() + timedelta(seconds=90)

    practitioner.reset_token = reset_token
    practitioner.token_expiration = expiration
    practitioner.save()

    # Send reset password link via email
    send_reset_password_email(email, reset_token)

    flash("Reset token sent to your email. YOU HAVE 1 MIN", category="success")
    return redirect(url_for("app_views.reset_password"))


# get the token from the url
@app_views.route(
    "/practitioner/reset_pass", methods=["GET", "POST"], strict_slashes=False
)
def reset_password():
    """This function resets the password after validating the token"""

    if request.method == "GET":
        return render_template("reset_password.html")
    pass_pattern = (
        r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$"
    )
    reset_token = request.form.get("token")
    new_password = request.form.get("password")
    confirm = request.form.get("confirm_password")
    if not re.match(pass_pattern, new_password):
        flash(
            "Password must be at least 8 characters long and contain at least one uppercase letter, one lowercase letter, one digit, and one special character",
            category="error",
        )
        return redirect(url_for("app_views.reset_password"))
    if confirm != new_password:
        flash("Password do not match", category="error")
        return redirect(url_for("app_views.reset_password"))
    if verify_reset_password(reset_token, new_password):
        flash("Password rest successful", category="succcess")
        return redirect(url_for("app_views.login_practitioner"))
    else:
        flash("Invalid token", category="error")
        return redirect(url_for("app_views.reset_password"))

# register child based on the parent_id
@app_views.route('/practitioner/parent/<parent_id>/child', methods=["GET", 'POST'], strict_slashes=False)
def reg_child(parent_id):
    if request.method == 'GET':
        user_id = request.cookies.get("Session")
        session = storage.get("Session", user_id)
        if not session or session.expiration_time < datetime.utcnow():
            flash("TIMEOUT", category="error")
            return redirect(url_for("app_views.login_practitioner"))   
        session.expiration_time = datetime.utcnow() + timedelta(minutes=2)
        storage.save()
        return render_template("zz.html")
    parent = storage.get("Parent", parent_id)
  
    if request.method == 'POST':
        data = request.form.to_dict()
        required_fields = ["first_name", "second_name", "date_of_birth"]
        for field in required_fields:
            if not data.get(field):
                flash(f"Missing {field.replace('_', ' ')}", "error")
                return render_template("zz.html")

        data["parent_id"] = parent_id
        new_child = Child(**data)
        new_child.save()
        date_of_birth = datetime.strptime(new_child.date_of_birth, '%Y-%m-%d')
        months = (datetime.now() - date_of_birth).days / 30
        if months > 0 and months < 6:
            vaccines = storage.all("Vaccine")
            for vaccine in vaccines.values():
                if vaccine.no_doses > 1:
                    for i in range(1, vaccine.no_doses):
                        vaccine_admin = Vaccine_administration(
                            vaccine_id=vaccine.id,
                            child_id=new_child.id,
                            confirmation_status="pending",
                        )
                        vaccine_admin.save()
                vaccine_admin = Vaccine_administration(
                    vaccine_id=vaccine.id,
                    child_id=new_child.id,
                    confirmation_status="pending",
                )
                vaccine_admin.save()
                
                
        else:
            return render_template("email.html")
        
        
        child_vaccine_records= new_child.vaccine_administrations
        week_1 = datetime.utcnow() + timedelta(days=3)
        week_6 = datetime.utcnow() + timedelta(days=42)
        week_10 = datetime.utcnow() + timedelta(days=70)
        week_14 = datetime.utcnow() + timedelta(weeks=14)
        month_6 = datetime.utcnow() + timedelta(weeks=24)
        month_9 = datetime.utcnow() + timedelta(weeks=36)
        age_lists= {
            "week_1": [],
            "week_6": [],
            "week_10": [],
            "week_14": [],
            "month_6": [],
            "month_9": [],
        }
        vaccination_lists = {
        "BCG": [],
        "OPV": [],
        "HEP B": [],
        "DPT": [],
        "HIB": [],
        "PNEUMOCOCCAL": [],
        "ROTAVIRUS": [],
        "VIT A": [],
        "MEASLES": [],
        "YELLOW FEVER": [],
        }
        if child_vaccine_records:
            for value in child_vaccine_records:
                vaccine = storage.get("Vaccine", value.vaccine_id)
                if vaccine:
                    vaccine_name = vaccine.names
                if vaccine_name in vaccination_lists:
                    vaccination_lists[vaccine_name].append(value)           
        vaccines_to_add = {
            "week_1": ["BCG", "OPV", "HEP B"],
            "week_6": ["DPT", "HIB", "HEP B", "OPV", "PNEUMOCOCCAL", "ROTAVIRUS"],
            "week_10": ["DPT", "HIB", "HEP B", "OPV", "PNEUMOCOCCAL", "ROTAVIRUS"],
            "week_14": ["DPT", "HIB", "HEP B", "OPV", "PNEUMOCOCCAL", "ROTAVIRUS"],
            "month_6": ["VIT A", "MEASLES"],
            "month_9": ["YELLOW FEVER"],
        }
        for age, vaccines in vaccines_to_add.items():
            for vaccine in vaccines:
                if vaccination_lists[vaccine]:
                    value = vaccination_lists[vaccine].pop(0)
                    if age == "week_1":
                        duedate = Duedate(due_date=week_1, vaccine_administration_id=value.id)
                        duedate.save()
                    elif age == "week_6":
                        duedate = Duedate(due_date=week_6, vaccine_administration_id=value.id)
                        duedate.save()
                    elif age == "week_10":
                        duedate = Duedate(due_date=week_10, vaccine_administration_id=value.id)
                        duedate.save()
                    elif age == "week_14":
                        duedate = Duedate(due_date=week_14, vaccine_administration_id=value.id)
                        duedate.save()
                    elif age == "month_6":
                        duedate = Duedate(due_date=month_6, vaccine_administration_id=value.id)
                        duedate.save()
                    elif age == "month_9":
                        duedate = Duedate(due_date=month_9, vaccine_administration_id=value.id)
                        duedate.save()
                
        flash("Child registered successfully immunization record created due date for notification set", "success")
        
        
    return redirect(url_for("app_views.search_parent_form"))


@app_views.route('/practitioner/parent/<parent_id>/children', methods=["GET"], strict_slashes=False)
def get_children(parent_id):
    user_id = request.cookies.get("Session")
    session = storage.get("Session", user_id)
    if not session or session.expiration_time < datetime.utcnow():
        flash("TIMEOUT", category="error")
        return redirect(url_for("app_views.login_practitioner"))   
    session.expiration_time = datetime.utcnow() + timedelta(minutes=2)
    storage.save()
    parent = storage.get("Parent", parent_id)
    if not parent:
        return jsonify({"error": "Parent not found"}), 404
    
    children = [child.to_dict() for child in parent.children]
    if not children:
        return jsonify({"error": "No children found"}), 404
    
    return jsonify(children), 200
# get all children in the system
@app_views.route('/practitioner/children', methods=["GET"], strict_slashes=False)
def get_all_children():
    """this function gets all the children in the system"""
    user_id = request.cookies.get("Session")
    session = storage.get("Session", user_id)
    if not session or session.expiration_time < datetime.utcnow():
        flash("TIMEOUT", category="error")
        return redirect(url_for("app_views.login_practitioner"))   
    session.expiration_time = datetime.utcnow() + timedelta(minutes=2)
    storage.save()
    children = storage.all("Child")
    if not children:
        return {"error": "No children found"}, 404
    children = [child.to_dict().json() for child in children]
    print(children)
    return jsonify(children, 200)

# get a child based on the child_id
@app_views.route('/practitioner/child/<child_id>', methods=["GET"], strict_slashes=False)
def geta_child(child_id):
    child = storage.get("Child", child_id)
    if not child:
        return {"error": "Child not found"}, 404
    return jsonify(child.to_dict()), 200

# add a link for the faqs
@app_views.route('/practitioner/faqs', methods=["GET"], strict_slashes=False)
def faqs():
    return render_template("faqs.html")

@app_views.route("/pract/parent/register", methods=["GET", "POST"], strict_slashes=False)
def parent_regist():
    if request.method == "GET":
        return render_template("parent.html")

    email = request.form.get("email")
    password = request.form.get("password")
    confirm_password = request.form.get("confirm_password")
    first_name = request.form.get("first_name")
    second_Name = request.form.get("second_Name")
    phone_number = request.form.get("phone_number")
    county = request.form.get("county")
    print(email)
    parent = storage.get_by_email("Parent", email)
    if parent:
        flash("The email has already been used!!!", category="error")
        return redirect(url_for("app_views.parent_regist"))
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
    return redirect(url_for("app_views.practitioner_dashboard"))


    
