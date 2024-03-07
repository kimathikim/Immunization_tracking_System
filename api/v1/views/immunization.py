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
from models.vaccine import Vaccine
from models.sessionManager import Session
from models.vaccineAdministration import Vaccine_administration
import re
from email.mime.text import MIMEText
import secrets
from datetime import datetime, timedelta
from models import storage
from models.sessionManager import Session
from datetime import datetime, timedelta

@app_views.route("/pratitioner/search/<child_id>/child", methods=["GET", "POST"], strict_slashes=False)
def vaccination_records(child_id):
    # Checking session validity
    user_id = request.cookies.get("Session")
    session = storage.get("Session", user_id)
    if not session or session.expiration_time < datetime.utcnow():
        flash("Session Ended. Please login again.", category="error")
        return redirect(url_for("app_views.login_practitioner"))
    session.expiration_time = datetime.utcnow() + timedelta(minutes=30)
    storage.save()
    
    child = storage.get("Child", child_id)
    practitioner = storage.get_by_email("Practitioner", session.email)
    print(practitioner)
    update_time = datetime.utcnow()
    child_vaccine_records = child.vaccine_administrations
    
    
    if request.method == "POST":
        record_id = request.form.get("record_id")
        for value in child_vaccine_records:
            if value.id == record_id:
                value.confirmation_status = "confirmed"
                value.practitioner_id = practitioner.id 
                value.administration_date = update_time
                value.practitioner_name = "Dr. "+practitioner.first_name
                storage.save()


        return redirect(url_for("app_views.vaccination_records", child_id=child_id, practitioner_name=practitioner.first_name))


    # Retrieving child and vaccination records
   
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
        print()
        for value in child_vaccine_records:
            vaccine = storage.get("Vaccine", value.vaccine_id)
            if vaccine:
                vaccine_name = vaccine.names
                if vaccine_name in vaccination_lists:
                    vaccination_lists[vaccine_name].append(value)
    

        
    return render_template("vaccination_record.html", vaccination_lists=vaccination_lists, child=child)
