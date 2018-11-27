from flask_wtf import FlaskForm
from wtforms import validators, StringField, IntegerField, BooleanField, SelectMultipleField
from application.ships.models import Ship

class ShipCreateForm(FlaskForm):
    name = StringField("Name", [validators.Length(min=1, max=256)])
    cost = IntegerField("Cost", [validators.NumberRange(min=0, max=2147483647)])
    command_capable = BooleanField("Command-capable")
    propulsion_type = StringField("Propulsion type", [validators.Length(min=1, max=256)])
    move = IntegerField("Move", [validators.NumberRange(min=0, max=2147483647)])
    delta_v = IntegerField("Delta-v", [validators.NumberRange(min=0, max=2147483647)])
    evasion_passive = IntegerField("Passive evasion", [validators.NumberRange(min=-2147483647, max=2147483647)])
    evasion_active = IntegerField("Active evasion", [validators.NumberRange(min=-2147483647, max=2147483647)])
    evasion_endurance = IntegerField("Evasion endurance", [validators.Optional(), validators.NumberRange(min=0, max=2147483647)])
    integrity = IntegerField("Integrity", [validators.NumberRange(min=0, max=2147483647)])
    primary_facing = StringField("Primary facing", [validators.Length(min=1, max=256)])
    armor_front = IntegerField("Front armor", [validators.NumberRange(min=0, max=2147483647)])
    armor_sides = IntegerField("Side armor", [validators.NumberRange(min=0, max=2147483647)])
    armor_back = IntegerField("Rear armor", [validators.NumberRange(min=0, max=2147483647)])

    # What exactly does coerce=int do?
    # This needs to be validated so that a ship belongs to at least one faction, not sure how
    factions = SelectMultipleField("Factions", coerce=int)

    class Meta:
        csrf = False