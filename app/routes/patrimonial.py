
from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt, get_jwt_identity
from ..extensions import db
from ..models import PatrolRoute, PatrolCheckpoint, PatrolCheck, AccessEvent, AssetIncident
from ..utils.security import role_required

bp = Blueprint("patrimonial", __name__)

def _cid(): return (get_jwt() or {}).get("company_id")

@bp.post("/routes")
@jwt_required()
@role_required("patrimonial","supervisor","admin","owner")
def create_route():
    d = request.get_json() or {}
    r = PatrolRoute(company_id=_cid(), name=d.get("name","Ronda"))
    db.session.add(r); db.session.commit()
    return {"id": r.id}, 201

@bp.post("/routes/<int:route_id>/checkpoints")
@jwt_required()
@role_required("patrimonial","supervisor","admin","owner")
def add_checkpoint(route_id):
    d = request.get_json() or {}
    cp = PatrolCheckpoint(route_id=route_id, name=d.get("name","Ponto"), lat=d.get("lat"), lon=d.get("lon"))
    db.session.add(cp); db.session.commit()
    return {"id": cp.id}, 201

@bp.post("/routes/<int:route_id>/check")
@jwt_required()
@role_required("patrimonial","supervisor","admin","owner")
def do_check(route_id):
    d = request.get_json() or {}
    uid = int(get_jwt_identity())
    chk = PatrolCheck(route_id=route_id, user_id=uid, checkpoint_id=d.get("checkpoint_id"))
    db.session.add(chk); db.session.commit()
    return {"id": chk.id}, 201

@bp.post("/access/events")
@jwt_required()
@role_required("patrimonial","supervisor","admin","owner")
def access_event():
    d = request.get_json() or {}
    ev = AccessEvent(company_id=_cid(), subject=d.get("subject"), badge=d.get("badge"), event=d.get("event","in"))
    db.session.add(ev); db.session.commit()
    return {"id": ev.id}, 201

@bp.post("/asset-incidents")
@jwt_required()
@role_required("patrimonial","supervisor","admin","owner")
def asset_incident():
    d = request.get_json() or {}
    ai = AssetIncident(company_id=_cid(), category=d.get("category"), description=d.get("description"))
    db.session.add(ai); db.session.commit()
    return {"id": ai.id}, 201
