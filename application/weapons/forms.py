from flask_wtf import FlaskForm
from wtforms import validators, StringField, IntegerField, BooleanField
from application.weapons.models import *

class LaserCreateForm(FlaskForm):
    name = StringField("Name", [validators.Length(min=1, max=256)])
    laser_dmg_missile = IntegerField("Anti-missile damage", [validators.NumberRange(min=0, max=2147483647)])

    class Meta:
        csrf = False

class MissileCreateForm(FlaskForm):
    missile_name = StringField("Name", [validators.Length(min=1, max=256)])
    volley = IntegerField("Volley", [validators.NumberRange(min=0, max=2147483647)])
    stores = IntegerField("Stores", [validators.NumberRange(min=0, max=2147483647)])

    class Meta:
        csrf = False
