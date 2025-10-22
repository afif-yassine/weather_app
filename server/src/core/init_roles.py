# server/src/core/init_roles.py
from sqlalchemy.orm import Session
from server.src.models.role_model import Role
from server.src.models.user_model import User
from server.src.core.security import get_password_hash

def init_roles(db: Session):
    """Initialise les rôles 'user' et 'admin'"""
    roles_to_create = ["user", "admin"]

    for role_name in roles_to_create:
        role = db.query(Role).filter(Role.name == role_name).first()
        if not role:
            db.add(Role(name=role_name))
            print(f"Création du rôle: {role_name}")

    db.commit()


def init_admin(db: Session, email: str, username: str, password: str):
    """Crée un utilisateur admin par défaut s'il n'existe pas"""
    user = db.query(User).filter(User.username == username).first()
    if not user:
        hashed_pw = get_password_hash(password)
        admin_role = db.query(Role).filter(Role.name == "admin").first()
        if not admin_role:
            raise Exception("Le rôle 'admin' n'existe pas, initialisez les rôles avant")

        user = User(
            email=email,
            username=username,
            hashed_password=hashed_pw,
            role=admin_role  # ✅ ici c'est l'objet Role
        )
        db.add(user)
        db.commit()
        print(f"Utilisateur admin '{username}' créé")
