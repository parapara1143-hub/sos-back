from flask import Blueprint, request, abort
from flask_jwt_extended import jwt_required
from ..extensions import db
from ..models.api_key import ApiKey
from ..config import Config

bp = Blueprint("apikeys", __name__)

@bp.post("")
@jwt_required()
def create_key():
    if not Config().ENABLE_PUBLIC_API_KEYS:
        abort(404)
    d = request.get_json() or {}
    ak = ApiKey(name=d.get("name","key"))
    db.session.add(ak); db.session.commit()
    return {"id": ak.id, "key": ak.key}, 201
