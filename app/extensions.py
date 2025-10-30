from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from flask_bcrypt import Bcrypt
from flask_socketio import SocketIO
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

db = SQLAlchemy()
migrate = Migrate()
jwt = JWTManager()
bcrypt = Bcrypt()
socketio = SocketIO(async_mode="eventlet")

limiter = Limiter(key_func=get_remote_address, default_limits=[])


from flask_jwt_extended import JWTManager
from .models.token import RefreshToken

# Attach callbacks after jwt = JWTManager() exists; override in app factory
