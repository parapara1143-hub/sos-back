from flask import Blueprint, request
from flask_jwt_extended import jwt_required
from ..extensions import db
from ..models.inspection import InspectionChecklist, InspectionItem, InspectionRecord
from ..utils.security import role_required

bp = Blueprint("inspections", __name__)

@bp.post("/checklists")
@jwt_required()
@role_required("tecnico_seg","supervisor","admin","owner")
def create_checklist():
    d = request.get_json() or {}
    c = InspectionChecklist(title=d.get("title"), company_id=d.get("company_id"))
    db.session.add(c); db.session.commit()
    for it in (d.get("items") or []):
        db.session.add(InspectionItem(checklist_id=c.id, text=it.get("text")))
    db.session.commit()
    return {"id": c.id}, 201

@bp.get("/checklists")
@jwt_required()
def list_checklists():
    cs = InspectionChecklist.query.order_by(InspectionChecklist.id.desc()).all()
    return {"items": [{"id": c.id, "title": c.title} for c in cs]}

@bp.post("/records")
@jwt_required()
@role_required("tecnico_seg","supervisor","admin","owner")
def create_record():
    d = request.get_json() or {}
    r = InspectionRecord(checklist_id=d.get("checklist_id"), user_id=d.get("user_id"), result=d.get("result") or {})
    db.session.add(r); db.session.commit()
    return {"id": r.id}, 201

@bp.get("/records")
@jwt_required()
def list_records():
    rs = InspectionRecord.query.order_by(InspectionRecord.id.desc()).limit(200).all()
    return {"items": [{"id": r.id, "checklist_id": r.checklist_id, "user_id": r.user_id, "created_at": r.created_at.isoformat()} for r in rs]}
