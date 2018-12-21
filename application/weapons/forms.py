from flask_wtf import FlaskForm
from wtforms import validators, StringField, IntegerField, BooleanField
from application.weapons.models import *

class LaserCreateForm(FlaskForm):
    name = StringField("Name", [validators.Length(min=1, max=256)])
    turreted = BooleanField("Turreted")
    laser_dmg_missile = IntegerField("Anti-missile damage", [validators.NumberRange(min=0, max=2147483647)])

    class Meta:
        csrf = False

class MissileCreateForm(FlaskForm):
    name = StringField("Name", [validators.Length(min=1, max=256)])
    volley = IntegerField("Volley", [validators.NumberRange(min=0, max=2147483647)])
    stores = IntegerField("Stores", [validators.NumberRange(min=0, max=2147483647)])

    class Meta:
        csrf = False

class CIWSCreateForm(FlaskForm):
    name = StringField("Name", [validators.Length(min=1, max=256)])
    dmg_missile = StringField("Anti-missile damage", [validators.Length(min=1, max=256)])
    dmg_ship = StringField("Anti-ship damage", [validators.Length(min=1, max=256)])

    class Meta:
        csrf = False

class AreaMissileCreateForm(FlaskForm):
    name = StringField("Name", [validators.Length(min=1, max=256)])
    am_range = IntegerField("Range", [validators.NumberRange(min=0, max=2147483647)])
    # Blank input is allowed for area missile damage, because they may be missing either
    # anti-ship or anti-missile capabilities.
    dmg_missile = StringField("Anti-missile damage", [validators.Length(max=256)])
    dmg_ship = StringField("Anti-ship damage", [validators.Length(max=256)])

    class Meta:
        csrf = False

class EwarCreateForm(FlaskForm):
    name = StringField("Name", [validators.Length(min=1, max=256)])

    class Meta:
        csrf = False