
from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from ..extensions import db
from ..models.incident import Incident, IncidentStatus, Attachment
from ..models.incident_event import IncidentEvent
from ..models.user import User
from ..sockets.events import broadcast_incident
from ..utils.security import role_required, require_company_scope

bp = Blueprint("incidents", __name__)

def company_id_from_claims():
    return (get_jwt() or {}).get("company_id")

@bp.post("")
@jwt_required()
@role_required("colaborador","brigadista","socorrista","tecnico_seg","supervisor","admin","owner")
@require_company_scope
def create_incident():
    from ..schemas.incident import IncidentCreate

    raw = request.get_json() or {}
    try:
        parsed = IncidentCreate(**raw)
    except Exception as e:
        return {"error":"invalid payload", "detail": str(e)}, 400
    d = parsed.model_dump()
    uid = int(get_jwt_identity())
    u = User.query.get(uid)
    i = Incident(
        title=d.get("title","Incident"),
        description=d.get("description"),
        status=IncidentStatus.open,
        lat=d.get("lat"), lon=d.get("lon"),
        reporter_id=uid,
        company_id=u.company_id
    )
    db.session.add(i); db.session.commit()
    db.session.add(IncidentEvent(incident_id=i.id, event='created', user_id=uid)); db.session.commit()
    for a in (d.get("attachments") or []):
        db.session.add(Attachment(incident_id=i.id, url=a.get("url"), label=a.get("label")))
    db.session.commit()
    broadcast_incident("incident.created", i)
    return {"id": i.id}, 201

@bp.get("")
@jwt_required()
def list_incidents():
    cid = company_id_from_claims()
    qs = Incident.query
    if cid is not None:
        qs = qs.filter(Incident.company_id==cid)
    incs = qs.order_by(Incident.id.desc()).limit(200).all()
    return {"items":[{"id":x.id,"title":x.title,"status":x.status.value,"lat":x.lat,"lon":x.lon} for x in incs]}

@bp.patch("/<int:incident_id>")
@jwt_required()
@role_required("brigadista","socorrista","tecnico_seg","supervisor","admin","owner")
def update_incident(incident_id):
    cid = company_id_from_claims()
    i = Incident.query.get_or_404(incident_id)
    if cid is not None and i.company_id != cid:
        return {"error":"forbidden"}, 403
    raw = request.get_json() or {}
    try:
        parsed = IncidentCreate(**raw)
    except Exception as e:
        return {"error":"invalid payload", "detail": str(e)}, 400
    d = parsed.model_dump()
    if "status" in d: i.status = IncidentStatus(d["status"])
    if "title" in d: i.title = d["title"]
    if "description" in d: i.description = d["description"]
    if "assignee_id" in d: i.assignee_id = d["assignee_id"]
    from ..models.incident import Attachment as Att
    db.session.commit()
    for a in (d.get("attachments") or []):
        db.session.add(Att(incident_id=i.id, url=a.get("url"), label=a.get("label")))
    db.session.commit()
    if "status" in d:
        db.session.add(IncidentEvent(incident_id=i.id, event=i.status.value, user_id=int(get_jwt_identity())));
        db.session.commit()
    broadcast_incident("incident.updated", i)
    return {"id": i.id, "status": i.status.value}
