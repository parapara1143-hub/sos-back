
from ..extensions import db

class Site(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    company_id = db.Column(db.Integer, nullable=False)

class Building(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    site_id = db.Column(db.Integer, nullable=False)
    name = db.Column(db.String(120), nullable=False)

class Floor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    building_id = db.Column(db.Integer, nullable=False)
    name = db.Column(db.String(120), nullable=False)
    level = db.Column(db.Integer, default=0)

class Zone(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    floor_id = db.Column(db.Integer, nullable=False)
    name = db.Column(db.String(120), nullable=False)
    attenuation = db.Column(db.Float, default=1.0)  # fator de atenuação para triangulação
