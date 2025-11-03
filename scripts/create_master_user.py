from app.extensions import db, bcrypt
from app.models.user import User
from app import create_app

# 🚀 Inicializa o app Flask
app = create_app()

with app.app_context():
    username = "Qsinclusao1143"
    password = "Poli@1143"
    email = "qsinclusao@admin.com"

    # Verifica se já existe
    existing = User.query.filter_by(username=username).first()
    if existing:
        print(f"⚠️ Usuário '{username}' já existe no banco de dados.")
    else:
        # Cria o usuário master
        user = User(
            username=username,
            email=email,
            role="master",
            company_id=None,
            is_active=True
        )
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        print(f"✅ Usuário master '{username}' criado com sucesso!")
