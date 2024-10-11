import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy


# setup project paths
MODULE_PATH = os.path.abspath(__file__)

# Create flask app instance
application = app = Flask(__name__)

# Add database
db = SQLAlchemy()
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

# Add secret key
app.config['SECRET_KEY'] = '59f063a2e5406614813c5b07e129fdrb'

# Add routes to app
from nanoplm import routes