from nanoplm import db
from nanoplm import app

with app.app_context():
    db.create_all()