from flask_wtf import FlaskForm
from wtforms import *
from application.ships.models import Ship

class ShipCreateForm(FlaskForm):
    name = StringField("Name")
    cost = IntegerField("Cost")
    command_capable = BooleanField("Command-capable")
    propulsion_type = StringField("Propulsion type")
    move = IntegerField("Move")
    delta_v = IntegerField("Delta-v")
    evasion_passive = IntegerField("Passive evasion")
    evasion_active = IntegerField("Active evasion")
    evasion_endurance = IntegerField("Evasion endurance")
    integrity = IntegerField("Integrity")
    primary_facing = StringField("Primary facing")
    armor_front = IntegerField("Front armor")
    armor_sides = IntegerField("Side armor")
    armor_back = IntegerField("Rear armor")
    weapon1_name = StringField("Weapon 1")
    weapon2_name = StringField("Weapon 2")
    weapon3_name = StringField("Weapon 3")

    class Meta:
        csrf = False

class ShipUpdateForm(FlaskForm):
    name = StringField("Name")
    cost = IntegerField("Cost")
    command_capable = BooleanField("Command-capable")
    propulsion_type = StringField("Propulsion type")
    move = IntegerField("Move")
    delta_v = IntegerField("Delta-v")
    evasion_passive = IntegerField("Passive evasion")
    evasion_active = IntegerField("Active evasion")
    evasion_endurance = IntegerField("Evasion endurance")
    integrity = IntegerField("Integrity")
    primary_facing = StringField("Primary facing")
    armor_front = IntegerField("Front armor")
    armor_sides = IntegerField("Side armor")
    armor_back = IntegerField("Rear armor")
    weapon1_name = StringField("Weapon 1")
    weapon2_name = StringField("Weapon 2")
    weapon3_name = StringField("Weapon 3")

    class Meta:
        csrf = False