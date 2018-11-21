from flask_wtf import FlaskForm
from wtforms import validators, StringField, IntegerField, BooleanField
from application.weapons.models import *

class LaserCreateForm(FlaskForm):
    laser_name = StringField("Name", [validators.Length(min=1, max=256)])
    laser_dmg_missile = IntegerField("Anti-missile damage", [validators.NumberRange(min=0)])

    class Meta:
        csrf = False
