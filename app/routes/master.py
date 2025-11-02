
from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt, get_jwt_identity, create_access_token
from datetime import timedelta
from ..extensions import db
from ..models.company import Company
from ..models.user import User, UserRole

bp = Blueprint("master", __name__)

def _is_master():
    claims = get_jwt() or {}
    return claims.get("role") == UserRole.owner.value

@bp.get("/companies")
@jwt_required()
def companies():
    if not _is_master():
        return {"error":"forbidden"}, 403
    items = Company.query.order_by(Company.name.asc()).all()
    return {"items": [{"id": c.id, "name": c.name} for c in items]}

@bp.post("/impersonate")
@jwt_required()
def impersonate():
    if not _is_master():
        return {"error":"forbidden"}, 403
    data = request.get_json() or {}
    company_id = data.get("company_id")
    if not company_id:
        return {"error":"company_id required"}, 400
    # Choose which role to grant during impersonation; default 'admin'
    role = data.get("role", UserRole.admin.value)
    uid = get_jwt_identity()
    # issue token limited time with company_id
    claims = {"role": role, "company_id": int(company_id), "impersonated_by": uid}
    token = create_access_token(identity=str(uid), additional_claims=claims, expires_delta=timedelta(hours=2))
    return {"access_token": token, "role": role, "company_id": int(company_id), "ttl_hours": 2}
