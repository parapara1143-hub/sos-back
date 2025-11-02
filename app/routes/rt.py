
from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from ..extensions import socketio
from datetime import datetime

bp = Blueprint("rt", __name__)

@bp.post("/location")
@jwt_required()
def post_location():
    payload = request.get_json() or {}
    user_id = get_jwt_identity()
    claims = get_jwt() or {}
    payload.setdefault("user_id", int(user_id) if user_id else None)
    payload.setdefault("company_id", claims.get("company_id"))
    payload.setdefault("ts", datetime.utcnow().isoformat()+"Z")
    # expected lat/lon
    if "lat" not in payload or "lon" not in payload:
        return {"error":"lat and lon required"}, 400
    # Broadcast to company room if available, else global
    room = None
    if payload.get("company_id") is not None:
        room = f"company:{payload['company_id']}"
    socketio.emit("location.update", payload, room=room, namespace="/rt")
    return {"status":"ok"}
