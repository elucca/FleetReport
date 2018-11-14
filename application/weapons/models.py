from application import db

# This class is a stub that is missing data that will eventually be provided in
# another table
class Laser(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(256), nullable=False)
    dmg_missile = db.Column(db.String(256), nullable=False)
    ship_id = db.Column(db.Integer, db.ForeignKey('ship.id'), nullable=False)


    def __init__(self, name, dmg_missile):
        self.name = name
        self.dmg_missile = dmg_missile

class Missile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(256), nullable=False)
    volley = db.Column(db.Integer, nullable=False)
    stores = db.Column(db.Integer, nullable=False)
    ship_id = db.Column(db.Integer, db.ForeignKey('ship.id'), nullable=False)

    def __init__(self, name, volley, stores):
        self.name = name
        self.volley = volley
        self.stores = stores

class CIWS(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(256), nullable=False)
    dmg_missile = db.Column(db.String(256), nullable=False)
    dmg_ship = db.Column(db.String(256), nullable=False)
    ship_id = db.Column(db.Integer, db.ForeignKey('ship.id'), nullable=False)

    def __init__(self, name, dmg_missile, dmg_ship):
        self.name = name
        self.dmg_missile = dmg_missile
        self.dmg_ship = dmg_ship

class AreaMissile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(256), nullable=False)
    range = db.Column(db.Integer, nullable=False)
    dmg_missile = db.Column(db.String(256), nullable=False)
    dmg_ship = db.Column(db.String(256), nullable=False)
    ship_id = db.Column(db.Integer, db.ForeignKey('ship.id'), nullable=False)

    def __init__(self, name, range, dmg_missile, dmg_ship):
        self.name = name
        self.range = range
        self.dmg_missile = dmg_missile
        self.dmg_ship = dmg_ship

# This class is a stub that is missing data that will eventually be provided in
# another table
class Ewar(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(256), nullable=False)
    ship_id = db.Column(db.Integer, db.ForeignKey('ship.id'), nullable=False)

    def __init__(self, name):
        self.name = name