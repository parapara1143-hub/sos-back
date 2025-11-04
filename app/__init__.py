from flask import Flask, request, g
from time import time
import uuid
import os
from flask_cors import CORS
from .extensions import db, migrate, jwt, bcrypt, socketio, limiter
from .config import Config
from .routes import register_routes
from flask_jwt_extended import get_jwt, get_jwt_identity, verify_jwt_in_request
from .sockets.events import register_socket_events
from .models.audit import AuditLog

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config())

    # Inicialização das extensões
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    bcrypt.init_app(app)
    socketio.init_app(app, cors_allowed_origins="*")
    limiter.init_app(app)

    # ============================================
    # ✅ CORS Configurado para TODOS os painéis
    # ============================================
    frontend_url = os.getenv("FRONTEND_URL", "https://sos-masterqs.vercel.app")

    CORS(app,
         resources={r"/api/*": {"origins": [
             frontend_url,
             "https://sos-masterqs.vercel.app",
             "https://sos-adminqs.vercel.app",
             "https://sos-mobileqs.vercel.app",
             "http://localhost:3000"
         ]}},
         supports_credentials=True)

    # ============================================
    # 🔐 Verificação de tokens de refresh
    # ============================================
    @jwt.token_in_blocklist_loader
    def check_if_token_revoked(jwt_header, jwt_payload):
        from .models.token import RefreshToken
        from datetime import datetime
        if jwt_payload.get('type') != 'refresh':
            return False
        jti = jwt_payload.get('jti')
        rt = RefreshToken.query.filter_by(jti=jti).first()
        return (rt is None) or rt.revoked or (rt.expires_at and rt.expires_at < datetime.utcnow())

    # ============================================
    # 📡 Registro de rotas e eventos de socket
    # ============================================
    register_routes(app)
    register_socket_events(socketio)

    # ============================================
    # 🧾 Auditoria automática de requisições
    # ============================================
    @app.before_request
    def _start_timer():
        g._t0 = time()
        g._req_id = str(uuid.uuid4())

    @app.after_request
    def audit(resp):
        try:
            dur = None
            if hasattr(g, "_t0"):
                dur = round((time() - g._t0) * 1000, 2)
            user_id = None
            role = None
            company_id = None
            try:
                verify_jwt_in_request(optional=True)
                user_id = get_jwt_identity()
                claims = get_jwt() or {}
                role = claims.get("role")
                company_id = claims.get("company_id")
            except Exception:
                pass
            al = AuditLog(
                path=request.path,
                method=request.method,
                status=resp.status_code,
                user_id=(int(user_id) if user_id else None)
            )
            db.session.add(al)
            db.session.commit()
        except Exception:
            db.session.rollback()
        resp.headers["X-Request-ID"] = getattr(g, "_req_id", "-")
        if hasattr(g, "_t0"):
            resp.headers["X-Response-Time-ms"] = str(round((time() - g._t0) * 1000, 2))
        return resp

    # ============================================
    # 🔍 Health Check
    # ============================================
    @app.get("/health")
    def health():
        return {"status": "ok", "version": "1.5.0"}

    # ============================================
    # 📁 Servir arquivos locais (uploads)
    # ============================================
    @app.get("/files/<path:filename>")
    def _files(filename):
        from flask import current_app, send_from_directory
        base = current_app.config.get("STORAGE_LOCAL_DIR", "uploads")
        return send_from_directory(base, filename)

    return app
