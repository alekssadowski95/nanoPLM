from nanoplm import db
from datetime import datetime


class Product(db.Model):
    # required
    id = db.Column(db.Integer, unique=True, nullable=False, primary_key=True)
    uuid = db.Column(db.String(32), unique=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    # default
    date_created = db.Column(db.DateTime, nullable= False, default=datetime.now)
    is_active = db.Column(db.Boolean, nullable=False, default=True)  
    # parameters
    description = db.Column(db.String(1000))
    type = db.Column(db.String(200))
    stammblattbreite = db.Column(db.Float)
    plattensitzhoehe = db.Column(db.Float)
    plattensitzlaenge = db.Column(db.Float)
    schnittbreite = db.Column(db.Float)
    aussendurchmesser = db.Column(db.Float)
    bohrungsdurchmesser = db.Column(db.Float)
    zaehnezahl = db.Column(db.Integer)

