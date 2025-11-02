
from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt, get_jwt_identity
from ..extensions import db
from ..models.wifi import LocationPing, WifiAccessPoint
from ..services.triangulation import estimate_location
from ..utils.security import role_required

bp = Blueprint("wifi", __name__)

def company_id_from_claims():
    return (get_jwt() or {}).get("company_id")

@bp.post("/triangulate")
@jwt_required()
def triangulate():
    d = request.get_json() or {}
    lat, lon = estimate_location(d.get("readings") or [])
    uid = int(get_jwt_identity())
    ping = LocationPing(user_id=uid, readings=d.get("readings"), estimated_lat=lat, estimated_lon=lon)
    db.session.add(ping); db.session.commit()
    return {"lat": lat, "lon": lon, "ping_id": ping.id}

@bp.post("/ap")
@jwt_required()
@role_required("tecnico_seg","supervisor","admin","owner")
def add_ap():
    d = request.get_json() or {}
    ap = WifiAccessPoint(ssid=d.get("ssid"), bssid=d.get("bssid"), lat=d.get("lat"), lon=d.get("lon"), company_id=d.get("company_id"))
    db.session.add(ap); db.session.commit()
    return {"id": ap.id}, 201

@bp.get("/ap")
@jwt_required()
def list_aps():
    cid = company_id_from_claims()
    qs = WifiAccessPoint.query
    if cid is not None:
        qs = qs.filter(WifiAccessPoint.company_id==cid)
    aps = qs.order_by(WifiAccessPoint.id.desc()).all()
    return {"items": [{"id": a.id, "ssid": a.ssid, "bssid": a.bssid, "lat": a.lat, "lon": a.lon} for a in aps]}
