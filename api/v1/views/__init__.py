from flask import Blueprint

app_views = Blueprint("app_views", __name__, url_prefix="/api/v1/")
home = Blueprint("home", __name__, url_prefix="/home")

# import storage engine and class

from models import storage
from models.healthcare_provider import Practitioner
from models.parent import Parent
from models.admin import Admin
from models.vaccineAdministration import Vaccine_administration
from models.vaccine import Vaccine
from models.diseases import Disease
from models.child import Child
from models.sessionManager import Session
from models.dueDate import Duedate



# import flask views
from api.v1.views.practitioner import *
from api.v1.views.parent import *
from api.v1.views.admin import *
from api.v1.views.immunization import *
from api.v1.views.parent_immunization import *
# from api.v1.views.notification_sys import *
