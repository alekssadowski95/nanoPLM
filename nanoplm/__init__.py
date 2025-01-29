import os
import sys

from flask import Flask
from flask_sqlalchemy import SQLAlchemy


# setup project paths
MODULE_DIR_PATH = os.path.dirname(os.path.abspath(__file__))

# Create flask app instance
application = app = Flask(__name__)

# Add database
db = SQLAlchemy()
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)


# database models
from datetime import datetime

class Component(db.Model):
    # required
    id = db.Column(db.Integer, unique=True, nullable=False, primary_key=True)
    uuid = db.Column(db.String(32), unique=True, nullable=False)
    name = db.Column(db.String(200), nullable=False)
    component_number = db.Column(db.String(200), nullable=False)
    # default
    date_created = db.Column(db.DateTime, nullable= False, default=datetime.now)
    is_active = db.Column(db.Boolean, nullable=False, default=True)
    status = db.Column(db.String(200), nullable=False, default="draft")  
    # optional
    description = db.Column(db.String(1000))
    files = db.Column(db.String(200))

class Instance(db.Model):
    # required
    id = db.Column(db.Integer, unique=True, nullable=False, primary_key=True)
    uuid = db.Column(db.String(32), unique=True, nullable=False)
    serial_number = db.Column(db.String(200), nullable=False)
    component = db.Column(db.String(200), nullable=False)
    # default
    date_created = db.Column(db.DateTime, nullable= False, default=datetime.now)
    is_active = db.Column(db.Boolean, nullable=False, default=True)  
    # optional
    client = db.Column(db.String(200))
    files = db.Column(db.String(200))    

class Client(db.Model):
    # required
    id = db.Column(db.Integer, unique=True, nullable=False, primary_key=True)
    uuid = db.Column(db.String(32), unique=True, nullable=False)
    name = db.Column(db.String(200), nullable=False)
    # default
    date_created = db.Column(db.DateTime, nullable= False, default=datetime.now)
    is_active = db.Column(db.Boolean, nullable=False, default=True)  
    # optional
    files = db.Column(db.String(200))

class File(db.Model):
    # required
    id = db.Column(db.Integer, unique=True, nullable=False, primary_key=True)
    uuid = db.Column(db.String(32), unique=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    # default
    date_created = db.Column(db.DateTime, nullable= False, default=datetime.now)
    is_active = db.Column(db.Boolean, nullable=False, default=True)  


# Add secret key
app.config['SECRET_KEY'] = 'afs87fas7bfsa98fbasbas98fh78oizu'

# Check user progres
app.config['NANOPLM_FIRST_STARTUP'] = True
app.config['NANOPLM_TUTORIAL_COMPLETE'] = False

# nanoPLM modules
app.config['NANOPLM_MODULE_FREECADCMD'] = False
app.config['NANOPLM_MODULE_FREECADGUI'] = False
app.config['NANOPLM_MODULE_PREPOMAX'] = False

# FreeCAD imports
app.config['SUPPORTED_FREECAD_VERSIONS'] = ['FreeCAD 0.21', 'FreeCAD 0.20'] # in order of preference, 1st is preferred
app.config['SELECTED_FREECAD_VERSION'] = 'None'

for version in reversed(app.config['SUPPORTED_FREECAD_VERSIONS']):
    version_path = 'C:/PROGRA~1/' + version
    if os.path.isdir(version_path) == True:
        print(version_path + '=' + str(os.path.isdir(version_path)))
        app.config['SELECTED_FREECAD_VERSION'] = version
    else:
        print(version_path + '=' + str(os.path.isdir(version_path)))

'''
# Add path to FreeCAD Python interface
# path to your FreeCAD.so or FreeCAD.dll file
FREECAD_ABS_PATH = 'C:/PROGRA~1/' + app.config['SELECTED_FREECAD_VERSION'] + '/bin'
sys.path.append(FREECAD_ABS_PATH)

# import the FreeCAD Python interface
try:
    import FreeCAD
    app.config['NANOPLM_MODULE_FREECADCMD'] = True
    print('The FreeCAD Python interface has been loaded')
except:
    app.config['NANOPLM_MODULE_FREECADGUI'] = False
    print('FreeCAD API not found. Please check the FREECAD_ABS_PATH variable.')

try:
    import Part
except:
    print('FreeCAD Part workbench not found.')

try:
    import MeshPart
except:
    print('FreeCAD MeshPart workbench not found.')

try:
    import Mesh
except:
    print('FreeCAD Mesh workbench not found.')

try:
    import PartDesign
except:
    print('FreeCAD PartDesign workbench (Windows) not found. (ignore if on Linux)')

try:
    import _PartDesign as PartDesign
except:
    print('FreeCAD _PartDesign workbench (Linux PPA) not found. (ignore if on Windows)')

try:
    import FreeCADGui
    app.config['NANOPLM_MODULE_FREECADGUI'] = True
    print('The FreeCAD GUI Python interface has been loaded')
except:
    app.config['NANOPLM_MODULE_FREECADGUI'] = False
    print('FreeCAD GUI API not found. Your server may not support the GUI API. Also, check the FREECAD_ABS_PATH variable.')
'''


# Add routes to app
from nanoplm import routes

# Launch FreeCAD GUI
'''
import subprocess
subprocess.Popen(['C:/PROGRA~1/' + app.config['SELECTED_FREECAD_VERSION'] + '/bin/FreeCAD.exe'])
'''


