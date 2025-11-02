
from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from ..extensions import db
from ..models import EvacuationPlan, MusterPoint, EvacuationEvent, EvacuationCheckin, EvacuationStatus, User
from ..utils.security import role_required, require_company_scope
from ..sockets.events import socketio

bp = Blueprint("evac", __name__)

def company_id_from_claims():
    return (get_jwt() or {}).get("company_id")

# Plans & points
@bp.post("/plans")
@jwt_required()
@role_required("supervisor","tecnico_seg","admin","owner")
@require_company_scope
def create_plan():
    d = request.get_json() or {}
    plan = EvacuationPlan(name=d.get("name","Plan"), company_id=company_id_from_claims())
    db.session.add(plan); db.session.commit()
    for mp in (d.get("muster_points") or []):
        p = MusterPoint(plan_id=plan.id, name=mp.get("name","Point"), lat=mp.get("lat"), lon=mp.get("lon"))
        db.session.add(p)
    db.session.commit()
    return {"id": plan.id}, 201

@bp.post("/events/start")
@jwt_required()
@role_required("supervisor","tecnico_seg","admin","owner")
@require_company_scope
def start_event():
    d = request.get_json() or {}
    uid = int(get_jwt_identity())
    ev = EvacuationEvent(plan_id=d.get("plan_id"), started_by=uid)
    db.session.add(ev); db.session.commit()
    socketio.emit("evacuation.started", {"event_id": ev.id, "plan_id": ev.plan_id}, namespace="/rt")
    return {"id": ev.id}, 201

@bp.post("/events/<int:event_id>/close")
@jwt_required()
@role_required("supervisor","tecnico_seg","admin","owner")
def close_event(event_id):
    ev = EvacuationEvent.query.get_or_404(event_id)
    ev.status = EvacuationStatus.closed
    from datetime import datetime
    ev.closed_at = datetime.utcnow()
    db.session.commit()
    socketio.emit("evacuation.closed", {"event_id": ev.id}, namespace="/rt")
    return {"ok": True}

@bp.post("/events/<int:event_id>/checkin")
@jwt_required()
def checkin(event_id):
    d = request.get_json() or {}
    uid = int(get_jwt_identity())
    ci = EvacuationCheckin(event_id=event_id, user_id=uid, method=d.get("method","manual"), lat=d.get("lat"), lon=d.get("lon"))
    db.session.add(ci); db.session.commit()
    socketio.emit("evacuation.checkin", {"event_id": event_id, "user_id": uid}, namespace="/rt")
    return {"id": ci.id}, 201

@bp.get("/events/<int:event_id>/status")
@jwt_required()
def status(event_id):
    total_checkins = EvacuationCheckin.query.filter_by(event_id=event_id).count()
    return {"event_id": event_id, "checkins": total_checkins}
