
from flask import Blueprint, make_response
from flask_jwt_extended import jwt_required
from ..extensions import db
from ..models import ASO, EvacuationEvent, EvacuationCheckin
from ..services.pdf import render_pdf

bp = Blueprint("pdf", __name__)

@bp.get("/ohs/aso/<int:aso_id>")
@jwt_required()
def aso_pdf(aso_id):
    a = ASO.query.get_or_404(aso_id)
    html = f"""<h1>ASO #{a.id}</h1><p>Emitido em: {a.issued_at}</p><p>Apto: {'Sim' if a.fit else 'Não'}</p><pre>{a.notes or ''}</pre>"""
    pdf = render_pdf(html)
    resp = make_response(pdf)
    resp.headers["Content-Type"] = "application/pdf"
    resp.headers["Content-Disposition"] = f"inline; filename=aso_{a.id}.pdf"
    return resp

@bp.get("/evac/events/<int:event_id>/report.pdf")
@jwt_required()
def evac_pdf(event_id):
    ev = EvacuationEvent.query.get_or_404(event_id)
    checks = EvacuationCheckin.query.filter_by(event_id=event_id).count()
    html = f"""<h1>Relatório de Evacuação #{ev.id}</h1>
    <p>Status: {ev.status.value}</p>
    <p>Check-ins: {checks}</p>"""
    pdf = render_pdf(html)
    resp = make_response(pdf)
    resp.headers["Content-Type"] = "application/pdf"
    resp.headers["Content-Disposition"] = f"inline; filename=evac_{ev.id}.pdf"
    return resp
