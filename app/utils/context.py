
from flask_jwt_extended import get_jwt_identity
from ..models.user import User

def current_user():
    uid = get_jwt_identity()
    if not uid: 
        return None
    try:
        return User.query.get(int(uid))
    except Exception:
        return None
