from flaskext.sqlalchemy import SQLAlchemy
from flaskext.login import UserMixin
from campaign import db

class MapObject(db.Model):
    __tablename__ = 'map_objects'
    id = db.Column(db.Integer, primary_key=True)
    x = db.Column(db.Integer)
    y = db.Column(db.Integer)
    type = db.Column(db.String(32), nullable=False)
    __mapper_args__ = {'polymorphic_on' : type}

class Terrain(MapObject):
    __tablename__ = 'terrains'
    __mapper_args__ = {'polymorphic_identity' : 'terrain'}
    terrain_id = db.Column(db.Integer, db.ForeignKey('map_objects.id'), primary_key=True)
    terrain_type = db.Column(db.String(32), nullable=False)

    def __init__(self, x, y, terrain):
        self.x = x
        self.y = y
        self.terrain_type = terrain

class Ship(MapObject):
    __tablename__ = 'ships'
    __mapper_args__ = {'polymorphic_identity' : 'ship'}
    ship_id = db.Column(db.Integer, db.ForeignKey('map_objects.id'), primary_key=True)

