from flask_wtf import FlaskForm
from wtforms import validators, StringField, IntegerField, BooleanField
from application.ships.models import Ship

class ShipCreateForm(FlaskForm):
    name = StringField("Name", [validators.Length(min=1, max=256)])
    cost = IntegerField("Cost", [validators.NumberRange(min=0)])
    command_capable = BooleanField("Command-capable")
    propulsion_type = StringField("Propulsion type", [validators.Length(min=1, max=256)])
    move = IntegerField("Move", [validators.NumberRange(min=0)])
    delta_v = IntegerField("Delta-v", [validators.NumberRange(min=0)])
    evasion_passive = IntegerField("Passive evasion")
    evasion_active = IntegerField("Active evasion")
    evasion_endurance = IntegerField("Evasion endurance", [validators.Optional(), validators.NumberRange(min=0)])
    integrity = IntegerField("Integrity", [validators.NumberRange(min=0)])
    primary_facing = StringField("Primary facing", [validators.Length(min=1, max=256)])
    armor_front = IntegerField("Front armor", [validators.NumberRange(min=0)])
    armor_sides = IntegerField("Side armor", [validators.NumberRange(min=0)])
    armor_back = IntegerField("Rear armor", [validators.NumberRange(min=0)])

    class Meta:
        csrf = False