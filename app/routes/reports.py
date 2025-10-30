
from flask import Blueprint, request, Response
from flask_jwt_extended import jwt_required, get_jwt
from datetime import datetime, timedelta
from ..models.incident import Incident
from ..models.inspection import InspectionRecord

bp = Blueprint("reports", __name__)

def parse_dt(s, default=None):
    if not s:
        return default
    return datetime.fromisoformat(s)

def _company_id():
    return (get_jwt() or {}).get("company_id")

@bp.get("/summary")
@jwt_required()
def summary():
    df = parse_dt(request.args.get("date_from"), datetime.min)
    dt = parse_dt(request.args.get("date_to"), datetime.max)
    q = Incident.query.filter(Incident.created_at>=df, Incident.created_at<=dt)
    cid = _company_id()
    if cid is not None: q = q.filter(Incident.company_id==cid)
    counts = {"open":0,"in_progress":0,"resolved":0,"cancelled":0}
    for i in q.all(): counts[i.status.value]+=1
    inspections = InspectionRecord.query.filter(InspectionRecord.created_at>=df, InspectionRecord.created_at<=dt).count()
    return {"incidents": counts, "inspections": inspections}

@bp.get("/summary.csv")
@jwt_required()
def summary_csv():
    df = parse_dt(request.args.get("date_from"), datetime.min)
    dt = parse_dt(request.args.get("date_to"), datetime.max)
    q = Incident.query.filter(Incident.created_at>=df, Incident.created_at<=dt)
    cid = _company_id()
    if cid is not None: q = q.filter(Incident.company_id==cid)
    counts = {"open":0,"in_progress":0,"resolved":0,"cancelled":0}
    for i in q.all(): counts[i.status.value]+=1
    inspections = InspectionRecord.query.filter(InspectionRecord.created_at>=df, InspectionRecord.created_at<=dt).count()
    csv = "metric,value\n" + "\n".join([f"incidents_{k},{v}" for k,v in counts.items()]) + f"\ninspections,{inspections}"
    return Response(csv, mimetype="text/csv")

@bp.get("/kpis")
@jwt_required()
def kpis():
    now = datetime.utcnow()
    df = now - timedelta(days=30)
    q = Incident.query.filter(Incident.created_at>=df)
    cid = _company_id()
    if cid is not None: q = q.filter(Incident.company_id==cid)
    total = q.count()
    # MTTA/MTTR simulados por falta de eventos; retornamos placeholders 0
    return {"window_days":30, "incidents_total": total, "mtta_sec": 0, "mttr_sec": 0}
