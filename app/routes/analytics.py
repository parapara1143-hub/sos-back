
from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt
from datetime import datetime, timedelta
from sqlalchemy import func
from ..models import Incident, IncidentStatus, IncidentEvent

bp = Blueprint("analytics", __name__)

def _cid(): return (get_jwt() or {}).get("company_id")

@bp.get("/mtta_mttr")
@jwt_required()
def mtta_mttr():
    # MTTA: tempo entre created -> in_progress/assigned
    # MTTR: tempo entre created -> resolved
    days = int((request.args.get("days") or 30))
    since = datetime.utcnow() - timedelta(days=days)
    cid = _cid()
    q_inc = Incident.query.filter(Incident.created_at>=since)
    if cid is not None: q_inc = q_inc.filter(Incident.company_id==cid)
    incs = q_inc.all()
    total_a = 0; count_a = 0
    total_r = 0; count_r = 0
    for inc in incs:
        evs = IncidentEvent.query.filter_by(incident_id=inc.id).order_by(IncidentEvent.created_at.asc()).all()
        t_created = next((e.created_at for e in evs if e.event=='created'), None)
        t_first_action = next((e.created_at for e in evs if e.event in ('in_progress','assigned')), None)
        t_resolved = next((e.created_at for e in evs if e.event=='resolved'), None)
        if t_created and t_first_action:
            total_a += (t_first_action - t_created).total_seconds(); count_a += 1
        if t_created and t_resolved:
            total_r += (t_resolved - t_created).total_seconds(); count_r += 1
    mtta = (total_a/count_a) if count_a else 0
    mttr = (total_r/count_r) if count_r else 0
    return {"window_days": days, "mtta_sec": int(mtta), "mttr_sec": int(mttr), "count_actions": count_a, "count_resolved": count_r}
