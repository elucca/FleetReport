from application import db

class Ship(db.Model):
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
    weapon1_name = db.Column(db.String(256), nullable=True)
    weapon2_name = db.Column(db.String(256), nullable=True)
    weapon3_name = db.Column(db.String(256), nullable=True)

    
    # Weapons are temporarily only strings. Eventually it'll be one-to-many relationships to weapon tables
    def __init__(self, name, cost, command_capable, propulsion_type, move, delta_v, evasion_passive, evasion_active, evasion_endurance, 
                 integrity, primary_facing, armor_front, armor_sides, armor_back, weapon1_name, weapon2_name, weapon3_name):
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
        self.weapon1_name = weapon1_name
        self.weapon2_name = weapon2_name
        self.weapon3_name = weapon3_name