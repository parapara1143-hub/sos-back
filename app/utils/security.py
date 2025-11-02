
from functools import wraps
from flask_jwt_extended import verify_jwt_in_request, get_jwt
from flask import abort

def role_required(*allowed):
    def deco(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            verify_jwt_in_request()
            claims = get_jwt() or {}
            role = claims.get("role")
            if role not in allowed:
                abort(403)
            return fn(*args, **kwargs)
        return wrapper
    return deco

def require_company_scope(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        verify_jwt_in_request()
        claims = get_jwt() or {}
        if "company_id" not in claims:
            abort(403)
        return fn(*args, **kwargs)
    return wrapper
