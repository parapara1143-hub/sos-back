
from datetime import datetime
from ..extensions import db

class OHSProgram(db.Model):  # PCMSO
    id = db.Column(db.Integer, primary_key=True)
    company_id = db.Column(db.Integer, nullable=False)
    title = db.Column(db.String(200), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Exam(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    kind = db.Column(db.String(60), nullable=False)  # admissional, periódico, demissional, mudança função, retorno
    scheduled_for = db.Column(db.DateTime)
    result = db.Column(db.JSON)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class ASO(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    issued_at = db.Column(db.DateTime, default=datetime.utcnow)
    fit = db.Column(db.Boolean, default=True)
    notes = db.Column(db.Text)

class RiskExposure(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    agent = db.Column(db.String(120), nullable=False)  # ruído, calor, químicos...
    intensity = db.Column(db.String(60))
    ppe = db.Column(db.String(200))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class CAT(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    description = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
