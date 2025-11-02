
from flask import Blueprint, request
from ..utils.hmacsig import verify_hmac
from ..sockets.events import emit_integration_event

bp = Blueprint("integrations", __name__)

@bp.post("/cameras/events")
def camera_event():
    verify_hmac()
    payload = request.get_json() or {}
    emit_integration_event("camera.event", payload)
    return {"ok": True}

@bp.post("/alarms/events")
def alarm_event():
    verify_hmac()
    payload = request.get_json() or {}
    emit_integration_event("alarm.event", payload)
    return {"ok": True}
