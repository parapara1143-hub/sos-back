
from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt
from ..services.notifications import send_push
from ..services.emailer import send_email
from ..models.device import DeviceToken
from ..models.user import User

bp = Blueprint("notify", __name__)

def tokens_for_filters(role=None, company_id=None, user_ids=None):
    q = DeviceToken.query.filter_by(active=True)
    if user_ids:
        q = q.filter(DeviceToken.user_id.in_(user_ids))
    if company_id is not None:
        # join with users to match company
        from ..extensions import db
        q = q.join(User, User.id==DeviceToken.user_id).filter(User.company_id==company_id)
    tokens = [d.token for d in q.all()]
    return tokens

@bp.post("/push")
@jwt_required()
def notify_push():
    d = request.get_json() or {}
    claims = get_jwt() or {}
    company_id = claims.get("company_id")
    tokens = d.get("tokens")
    if not tokens:
        # build by filters (role not implemented here for simplicity; could be added by join on User.role)
        tokens = tokens_for_filters(company_id=company_id, user_ids=d.get("user_ids"))
    ok, resp = send_push(tokens or [], d.get("title"), d.get("body"), d.get("data"))
    return {"ok": ok, "response": resp}, (200 if ok else 400)

@bp.post("/email")
@jwt_required()
def notify_email():
    d = request.get_json() or {}
    ok, resp = send_email(d.get("to"), d.get("subject"), d.get("html"))
    return {"ok": ok, "response": resp}, (200 if ok else 400)
