#!/usr/bin/python3

"""App to register blueprint and start Flask"""

from flask import (
    Flask,
    make_response,
    jsonify,
    redirect,
    url_for,
    request,
    flash,
    render_template,
)
from flask_bcrypt import Bcrypt
from flask_bcrypt import Bcrypt
from flask_cors import CORS
from models import storage
from api.v1.views import app_views
from flask_mail import Mail
from os import getenv
from api.v1.views.practitioner import app_config
import os
from dotenv import load_dotenv

load_dotenv()


email = os.getenv("EMAIL")  
password = os.getenv("PASSWORD")


app = Flask(__name__)

# Initialize Flask-Login


# Configure secret key and mail settings
app.config["SECRET_KEY"] = app_config
app.config["MAIL_SERVER"] = "smtp.gmail.com"
app.config["MAIL_PORT"] = 587
app.config["MAIL_USERNAME"] = email
app.config["MAIL_PASSWORD"] = password
app.config["MAIL_USE_TLS"] = True
app.config["MAIL_USE_SSL"] = False
app.config["UPLOAD_FOLDER"] = "static/profile_pictures"
app.config["SESSION_TYPE"] = "sqlalchemy"
app.config["SESSION_SQLALCHEMY"] = None


# Initialize Flask-Mail
mail = Mail(app)

# Enable CORS
CORS(app, origins="0.0.0.0")

# Register blueprint
app.register_blueprint(app_views)


# Teardown app context
@app.teardown_appcontext
def teardown_db(exception):
    """Close all query after each session"""
    storage.close()


# Error handler for 404
@app.errorhandler(404)
def page_not_found(error):
    """Return JSON formatted 404 status code response"""
    return render_template("404.html", error=error)


if __name__ == "__main__":
    app.run(
        host=getenv("IMS_API_HOST", "0.0.0.0"),
        port=int(getenv("IMS_API_PORT", "5000")),
        threaded=True,
        debug=True,
    )