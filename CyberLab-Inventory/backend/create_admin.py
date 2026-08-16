from app.core.database import SessionLocal
from app.models.user import User
from app.core.security import get_password_hash

db = SessionLocal()

existing_admin = db.query(User).filter(User.username == "admin").first()

if not existing_admin:
    admin_user = User(
        username="admin",
        email="admin@cyberlab.local",
        full_name="Administrateur CyberLab",
        role="Admin",
        is_active=True,
        hashed_password=get_password_hash("admin123")
    )
    db.add(admin_user)
    db.commit()
    print("✅ Compte administrateur créé avec succès !")
    print("Username: admin")
    print("Password: admin123")
else:
    print("ℹ️ Le compte administrateur existe déjà.")

db.close()
