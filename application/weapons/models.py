from application import db

# Make an abstract base class to inherit from eventually, doesn't work right now
"""
class Weapon(db.Model):
    __abstract__ = True

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(256), nullable=False)
    ship_id = db.Column(db.Integer, db.ForeignKey('ship.id'), nullable=False)
    def __init__(self, name, ship_id):
        self.name = name
        self.ship_id = ship_id
"""

# This class is a stub that is missing data that will eventually be provided in
# another table
class Laser(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(256), nullable=False)
    laser_dmg_missile = db.Column(db.String(256), nullable=False)
    ship_id = db.Column(db.Integer, db.ForeignKey('ship.id'), nullable=False)

    def __init__(self, name, dmg_missile, ship_id):
        self.name = name
        self.laser_dmg_missile = dmg_missile
        self.ship_id = ship_id

"""
class Missile(Weapon):
    volley = db.Column(db.Integer, nullable=False)
    stores = db.Column(db.Integer, nullable=False)

    def __init__(self, name, volley, stores, ship_id):
        Weapon.__init__(self, name, ship_id)
        self.volley = volley
        self.stores = stores

class CIWS(Weapon):
    dmg_missile = db.Column(db.String(256), nullable=False)
    dmg_ship = db.Column(db.String(256), nullable=False)

    def __init__(self, name, dmg_missile, dmg_ship, ship_id):
        Weapon.__init__(self, name, ship_id)
        self.CIWS_dmg_missile = dmg_missile
        self.CIWS_dmg_ship = dmg_ship

class AreaMissile(Weapon):
    range = db.Column(db.Integer, nullable=False)
    AM_dmg_missile = db.Column(db.String(256), nullable=False)
    AM_dmg_ship = db.Column(db.String(256), nullable=False)

    def __init__(self, name, range, dmg_missile, dmg_ship, ship_id):
        Weapon.__init__(self, name, ship_id)
        self.range = range
        self.dmg_missile = dmg_missile
        self.dmg_ship = dmg_ship

# This class is a stub that is missing data that will eventually be provided in
# another table
class Ewar(Weapon):

    def __init__(self, name, ship_id):
        Weapon.__init__(self, name, ship_id)
"""