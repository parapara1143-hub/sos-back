
from flask import Blueprint, request
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity, get_jwt
from ..extensions import db, bcrypt, limiter
from ..models.user import User
from ..models.token import RefreshToken
from datetime import datetime, timedelta

bp = Blueprint("auth", __name__)

@bp.post("/login")
@limiter.limit("20/minute")
def login():
    data = request.get_json() or {}
    email = data.get("email"); password = data.get("password")
    remember = bool(data.get("remember", True))
    if not email or not password:
        return {"error": "email and password required"}, 400
    u = User.query.filter_by(email=email).first()
    if not u or not bcrypt.check_password_hash(u.password_hash, password):
        return {"error": "invalid credentials"}, 401
    claims = {"role": u.role.value, "company_id": u.company_id}
    access = create_access_token(identity=str(u.id), additional_claims=claims)
    # refresh exp: 30d default; if not remember, 1d
    if remember:
        refresh = create_refresh_token(identity=str(u.id), additional_claims=claims)
        jti = get_jwt(refresh_token=refresh)["jti"]
        rt = RefreshToken(jti=jti, user_id=u.id, revoked=False, expires_at=datetime.utcnow()+timedelta(days=30))
    else:
        refresh = create_refresh_token(identity=str(u.id), additional_claims=claims)
        jti = get_jwt(refresh_token=refresh)["jti"]
        rt = RefreshToken(jti=jti, user_id=u.id, revoked=False, expires_at=datetime.utcnow()+timedelta(days=1))
    db.session.add(rt); db.session.commit()
    return {"access_token": access, "refresh_token": refresh, "role": u.role.value, "company_id": u.company_id}

@bp.post("/refresh")
@jwt_required(refresh=True)
def refresh():
    uid = int(get_jwt_identity())
    claims_in = get_jwt()
    jti_old = claims_in.get("jti")
    # revoke old
    from ..models.token import RefreshToken
    rt = RefreshToken.query.filter_by(jti=jti_old, user_id=uid).first()
    if not rt or rt.revoked:
        return {"error":"refresh token invalidated"}, 401
    rt.revoked = True
    db.session.add(rt)
    # issue new refresh (rotation)
    from ..models.user import User
    u = User.query.get(uid)
    claims = {"role": u.role.value, "company_id": u.company_id}
    new_access = create_access_token(identity=str(u.id), additional_claims=claims)
    new_refresh = create_refresh_token(identity=str(u.id), additional_claims=claims)
    jti_new = get_jwt(refresh_token=new_refresh)["jti"]
    from datetime import datetime, timedelta
    rt2 = RefreshToken(jti=jti_new, user_id=u.id, revoked=False, expires_at=datetime.utcnow()+timedelta(days=30))
    db.session.add(rt2); db.session.commit()
    return {"access_token": new_access, "refresh_token": new_refresh}
