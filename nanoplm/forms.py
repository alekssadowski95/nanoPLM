from flask_wtf import FlaskForm
from wtforms.fields import StringField, TextAreaField, RadioField, SubmitField, SelectField
from wtforms.validators import DataRequired, Length


class CreateComponentForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(min=1, max=200)])
    description = StringField('Beschreibung', validators=[DataRequired(), Length(min=1, max=1000)])
    component_number = SelectField('Nummernkreis', choices = [("10.10.10", "10.10.10 (Sicherheitsschraube - VPE)"),
                                                              ("10.10.20", "10.10.20 (Sicherheitsschraube - Schraube)"),
                                                              ("10.10.30", "10.10.30 (Sicherheitsschraube - Einwegeinsatz)")])
    submit = SubmitField('Erstellen')

class CreateComponentInstanceForm(FlaskForm):
    component_uuid = SelectField('Komponente')
    client_uuid = SelectField('Kunde')
    submit = SubmitField('Erstellen')

class CreateClientForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(min=1, max=200)])
    submit = SubmitField('Erstellen')

class CreateFileForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(min=1, max=200)])
    submit = SubmitField('Erstellen')

'''
Old stuff
'''
class CreateProductForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(min=1, max=200)])
    description = StringField('Beschreibung', validators=[DataRequired(), Length(min=1, max=1000)])
    type = StringField('Typ', validators=[DataRequired(), Length(min=1, max=200)])
    stammblattbreite = StringField('Stammblattbreite (mm)')
    plattensitzhoehe = StringField('Plattensitzhöhe (mm)')
    plattensitzlaenge = StringField('Plattensitzlänge (mm)')
    plattensitzwinkel = StringField('Plattensitzwinkel (°)')
    schnittbreite = StringField('Schnittbreite (mm)')
    aussendurchmesser = StringField('Außendurchmesser (mm)')
    bohrungsdurchmesser = StringField('Bohrungsdurchmesser (mm)')
    zaehnezahl = StringField('Zähnezahl')
    submit = SubmitField('Erstellen')