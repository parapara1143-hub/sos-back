from app import create_app
from app.extensions import db, bcrypt
from app.models.user import User, UserRole
from app.models.company import Company
from app.models.wifi import WifiAccessPoint

app = create_app()
with app.app_context():
    c = Company(name="Demo Industries", cnpj="00.000.000/0001-00")
    db.session.add(c); db.session.commit()

    pwd = bcrypt.generate_password_hash("123456").decode()
    users = [
        ("owner@sos.local","Owner",UserRole.owner),
        ("admin@sos.local","Admin",UserRole.admin),
        ("supervisor@sos.local","Supervisor",UserRole.supervisor),
        ("tecnico@sos.local","Técnico Seg",UserRole.tecnico_seg),
        ("brigadista@sos.local","Brigadista",UserRole.brigadista),
        ("socorrista@sos.local","Socorrista",UserRole.socorrista),
        ("medico@sos.local","Médico",UserRole.medico),
        ("patrimonial@sos.local","Patrimonial",UserRole.patrimonial),
        ("colaborador@sos.local","Colaborador",UserRole.colaborador),
    ]
    for email, name, role in users:
        db.session.add(User(email=email, name=name, password_hash=pwd, role=role, company_id=c.id))

    aps = [
        WifiAccessPoint(ssid="AP-A", bssid="AA:BB:CC:DD:EE:01", lat=-19.97, lon=-44.20, company_id=c.id),
        WifiAccessPoint(ssid="AP-B", bssid="AA:BB:CC:DD:EE:02", lat=-19.969, lon=-44.199, company_id=c.id),
        WifiAccessPoint(ssid="AP-C", bssid="AA:BB:CC:DD:EE:03", lat=-19.971, lon=-44.201, company_id=c.id),
    ]
    db.session.add_all(aps); db.session.commit()
    print("Seed OK. owner@sos.local / 123456")
