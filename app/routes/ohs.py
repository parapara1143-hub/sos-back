
from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt
from ..extensions import db
from ..models import OHSProgram, Exam, ASO, RiskExposure, CAT
from ..utils.security import role_required

bp = Blueprint("ohs", __name__)

def _cid(): return (get_jwt() or {}).get("company_id")

@bp.post("/programs")
@jwt_required()
@role_required("medico","supervisor","admin","owner")
def create_program():
    d = request.get_json() or {}
    p = OHSProgram(company_id=_cid(), title=d.get("title","PCMSO"))
    db.session.add(p); db.session.commit()
    return {"id": p.id}, 201

@bp.post("/exams")
@jwt_required()
@role_required("medico","supervisor","admin","owner")
def schedule_exam():
    d = request.get_json() or {}
    e = Exam(user_id=d.get("user_id"), kind=d.get("kind","periodico"), scheduled_for=d.get("scheduled_for"))
    db.session.add(e); db.session.commit()
    return {"id": e.id}, 201

@bp.post("/aso")
@jwt_required()
@role_required("medico","supervisor","admin","owner")
def issue_aso():
    d = request.get_json() or {}
    a = ASO(user_id=d.get("user_id"), fit=bool(d.get("fit", True)), notes=d.get("notes"))
    db.session.add(a); db.session.commit()
    return {"id": a.id}, 201

@bp.post("/exposure")
@jwt_required()
@role_required("medico","tecnico_seg","supervisor","admin","owner")
def add_exposure():
    d = request.get_json() or {}
    r = RiskExposure(user_id=d.get("user_id"), agent=d.get("agent"), intensity=d.get("intensity"), ppe=d.get("ppe"))
    db.session.add(r); db.session.commit()
    return {"id": r.id}, 201

@bp.post("/cat")
@jwt_required()
@role_required("medico","supervisor","admin","owner")
def create_cat():
    d = request.get_json() or {}
    c = CAT(user_id=d.get("user_id"), description=d.get("description"))
    db.session.add(c); db.session.commit()
    return {"id": c.id}, 201
