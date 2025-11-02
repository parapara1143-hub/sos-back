
from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from ..extensions import db
from ..models.device import DeviceToken

bp = Blueprint("devices", __name__)

@bp.post("/register")
@jwt_required()
def register():
    uid = int(get_jwt_identity())
    d = request.get_json() or {}
    token = d.get("token"); platform = d.get("platform")
    if not token:
        return {"error":"token required"}, 400
    dt = DeviceToken.query.filter_by(token=token).first()
    if not dt:
        dt = DeviceToken(user_id=uid, platform=platform, token=token, active=True)
        db.session.add(dt)
    else:
        dt.user_id = uid; dt.platform = platform; dt.active = True
    db.session.commit()
    return {"id": dt.id}

@bp.delete("/register")
@jwt_required()
def unregister():
    d = request.get_json() or {}
    token = d.get("token")
    if not token:
        return {"error":"token required"}, 400
    dt = DeviceToken.query.filter_by(token=token).first()
    if not dt:
        return {"ok": True}
    dt.active = False
    db.session.commit()
    return {"ok": True}
