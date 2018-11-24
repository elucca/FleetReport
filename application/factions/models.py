from application import db

# Associative entity for many-to-many relationship betwen factions and ships
factionships = db.Table('factionship',
    db.Column('faction_id', db.Integer, db.ForeignKey('faction.id'), primary_key=True),
    db.Column('ship_id', db.Integer, db.ForeignKey('ship.id'), primary_key=True)
)

class Faction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(256), nullable=False)
    factionships = db.relationship('Faction', secondary=factionships, lazy=True,
        backref=db.backref('ships', lazy=True))