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
# Add path to FreeCAD Python interface
# path to your FreeCAD.so or FreeCAD.dll file
FREECAD_ABS_PATH = 'C:/PROGRA~1/FreeCAD 0.21/bin'
sys.path.append(FREECAD_ABS_PATH)

# import the FreeCAD Python interface
try:
    import FreeCAD
    app.config['NANOPLM_MODULE_FREECADCMD'] = True
    print('The FreeCAD Python interface has been loaded')
except ValueError:
    print('FreeCAD library not found. Please check the FREECADPATH variable in the import script is correct')

try:
    import Part
    import MeshPart
    import Mesh
except:
    print('One of the FreeCAD dependencies is missing (Part, MeshPart, Mesh)')

try:
    import PartDesign
except:
    print('PartDesign (Windows) could not be imported (ignore if on Linux)')

try:
    import _PartDesign as PartDesign
except:
    print('_PartDesign (Linux PPA) could not be imported (ignore if on Windows)')

# Add routes to app
from nanoplm import routes