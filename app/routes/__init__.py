
from .auth import bp as auth_bp
from .users import bp as users_bp
from .incidents import bp as incidents_bp
from .notifications import bp as notify_bp
from .chat import bp as chat_bp
from .wifi import bp as wifi_bp
from .api_keys import bp as apikeys_bp
from .inspections import bp as inspections_bp
from .integrations import bp as integrations_bp
from .reports import bp as reports_bp
from .files import bp as files_bp
from .analytics import bp as analytics_bp
from .pdf import bp as pdf_bp
from .devices import bp as devices_bp
from .evacuation import bp as evac_bp
from .ohs import bp as ohs_bp
from .patrimonial import bp as patr_bp

def register_routes(app):
    app.register_blueprint(auth_bp, url_prefix="/api/auth")
    app.register_blueprint(users_bp, url_prefix="/api/users")
    app.register_blueprint(incidents_bp, url_prefix="/api/incidents")
    app.register_blueprint(notify_bp, url_prefix="/api/notify")
    app.register_blueprint(chat_bp, url_prefix="/api/chat")
    app.register_blueprint(wifi_bp, url_prefix="/api/wifi")
    app.register_blueprint(apikeys_bp, url_prefix="/api/apikeys")
    app.register_blueprint(inspections_bp, url_prefix="/api/inspections")
    app.register_blueprint(integrations_bp, url_prefix="/api/integrations")
    app.register_blueprint(reports_bp, url_prefix="/api/reports")
    app.register_blueprint(files_bp, url_prefix="/api/files")
    app.register_blueprint(analytics_bp, url_prefix="/api/analytics")
    app.register_blueprint(pdf_bp, url_prefix="/api/pdf")
    app.register_blueprint(devices_bp, url_prefix="/api/devices")
    app.register_blueprint(evac_bp, url_prefix="/api/evac")
    app.register_blueprint(ohs_bp, url_prefix="/api/ohs")
    app.register_blueprint(patr_bp, url_prefix="/api/patrimonial")
