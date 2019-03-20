from application import db
from application.models import BaseModel

class Ship(BaseModel):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(256), nullable=False)
    cost = db.Column(db.Integer, nullable=False)
    command_capable = db.Column(db.Boolean, nullable=False)
    propulsion_type = db.Column(db.String(256), nullable=False)
    move = db.Column(db.Integer, nullable=False)
    delta_v = db.Column(db.Integer, nullable=False)
    evasion_passive = db.Column(db.Integer, nullable=False)
    evasion_active = db.Column(db.Integer, nullable=False)
    evasion_endurance = db.Column(db.Integer, nullable=True)
    integrity = db.Column(db.Integer, nullable=False)
    primary_facing = db.Column(db.String(256), nullable=False)
    armor_front = db.Column(db.Integer, nullable=False)
    armor_sides = db.Column(db.Integer, nullable=False)
    armor_back = db.Column(db.Integer, nullable=False)
    
    card = db.relationship('ShipCard', backref='ship', lazy=True)

    # Weapons
    lasers = db.relationship('Laser', cascade="all, delete, delete-orphan", backref='ship', lazy=True)
    missiles = db.relationship('Missile', backref='ship', lazy=True)
    CIWSs = db.relationship('CIWS', backref='ship', lazy=True)
    area_missiles = db.relationship('AreaMissile', backref='ship', lazy=True)
    ewars = db.relationship('Ewar', backref='ship', lazy=True)

    # Fields for serialization
    _default_fields = [
        "name",
        "cost",
        "command_capable",
        "propulsion_type",
        "move",
        "delta_v",
        "evasion_passive",
        "evasion_active",
        "evasion_endurance",
        "integrity",
        "primary_facing",
        "lasers",
        "missiles",
        "CIWSs",
        "area_missiles",
        "ewars",
        "armor_front",
        "armor_sides",
        "armor_back"
    ]

    _hidden_fields = [
        "id",
        "card",
        "factions"
    ]

    def __init__(self, name, cost, command_capable, propulsion_type, move, delta_v, evasion_passive, evasion_active, evasion_endurance, 
                 integrity, primary_facing, armor_front, armor_sides, armor_back):
        self.name = name
        self.cost = cost
        self.command_capable = command_capable
        self.propulsion_type = propulsion_type
        self.move = move
        self.delta_v = delta_v
        self.evasion_passive = evasion_passive
        self.evasion_active = evasion_active
        self.evasion_endurance = evasion_endurance
        self.integrity = integrity
        self.primary_facing = primary_facing
        self.armor_front = armor_front
        self.armor_sides = armor_sides
        self.armor_back = armor_back

# This table contains the file path to a ship's card, if one exists
class ShipCard(BaseModel):
    __tablename__ = 'shipcard'

    id = db.Column(db.Integer, primary_key=True)
    filepath = db.Column(db.Text, nullable=False)
    ship_id = db.Column(db.Integer, db.ForeignKey('ship.id'), nullable=False, index=True)

    def __init__(self, filepath, ship_id):
        self.filepath = filepath
        self.ship_id = ship_id