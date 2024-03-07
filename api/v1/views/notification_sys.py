"""This module contains the notification system for the application"""
from models.parent import Parent
from models.vaccineAdministration import Vaccine_administration
from email.mime.text import MIMEText
import secrets
from datetime import datetime, timedelta
from models import storage
from models.dueDate import Duedate
from datetime import datetime, timedelta
import smtplib
import pytz
import schedule
import time

myEmail = "briankimathi94@gmail.com"
passwd = "uqiv dykn sntz ewyq"
smtp_server = 'smtp.gmail.com'
port = 587

def send_reminder_email(details_list):
    """This function sends an email reminder to parents about upcoming vaccinations"""
    try:
        for details in details_list:
            msg = MIMEText(f"Dear {details[0]},\n\nThis is a friendly reminder that your child: {details[2]} has vaccinations that are due on {datetime.now(pytz.utc) + timedelta(days=2)}. That is in 2 days.\n\nPlease ensure to check your IMS portal for more details.\n\nBest regards,\nYour Healthcare Provider")
            msg['Subject'] = "Friendly Reminder: Vaccination Due Soon"
            msg['From'] = myEmail
            msg['To'] = details[1]

            with smtplib.SMTP(smtp_server, port) as server:
                server.starttls()
                server.login(myEmail, passwd)
                server.send_message(msg)
    except Exception as e:
        print(f"An error occurred while sending email: {e}")
    finally:
        print("Congratulations, you tried")

def get_nonVaccinated_children():
    """This function get all children that have not been vaccinated"""
    vaccination_pending = []
    immunization_record = storage.all(Vaccine_administration)
    for record in immunization_record.values():
        if record.confirmation_status == "pending":
            vaccination_pending.append(record)
    return vaccination_pending

def get_due_dates():
    """This function gets all due dates for children"""
    due_dates = list(storage.all(Duedate).values())
    return due_dates

def get_parents():
    """This function gets all the parents in the system"""
    return list(storage.all(Parent).values())

wazazi = get_parents()
wakati = get_due_dates()
non_immunized = get_nonVaccinated_children()


def get_child_id(wakati, non_immunized):
    """This function returns the child id for non-immunized children with due dates within 3 days"""
    child_ids = []
    for date in wakati:
        time = datetime.strptime(date.due_date, '%Y-%m-%d %H:%M:%S.%f')
        remaining_time = time - datetime.utcnow()
        if remaining_time.days < 3:
            child_ids.extend(record.child_id for record in non_immunized if record.id == date.vaccine_administration_id)
    return child_ids

children_id = get_child_id(wakati, non_immunized)

def email_childID(children_id, wazazi):
    """This function returns the email and first name of parents for each child name"""
    email_first_name = []
    child_ids_set = set(children_id)
    for mzazi in wazazi:
        for child in mzazi.children:
            if child.id in child_ids_set:
                email_first_name.append((mzazi.first_name, mzazi.email, child.first_name))
    return email_first_name
                
email_childName = email_childID(children_id, wazazi)



send_reminder_email(email_childName)

