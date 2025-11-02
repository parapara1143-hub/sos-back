from flask import Blueprint
from flask_jwt_extended import jwt_required, get_jwt_identity
from ..models.user import User, UserRole

bp = Blueprint("users", __name__)

@bp.get("/me")
@jwt_required()
def me():
    uid = get_jwt_identity(); u = User.query.get(int(uid))
    return {"id": u.id, "email": u.email, "name": u.name, "role": u.role.value}

@bp.get("/role/<role>")
@jwt_required()
def list_by_role(role):
    try: r = UserRole(role)
    except Exception: return {"error": "invalid role"}, 400
    users = User.query.filter_by(role=r).all()
    return {"items": [{"id": x.id, "name": x.name, "email": x.email, "role": x.role.value} for x in users]}
