from datetime import datetime
from ..extensions import db

class Company(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    cnpj = db.Column(db.String(32))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
