from app.core.security import hash_password
from app.db.database import Base, SessionLocal, engine
from app.models.user import User

Base.metadata.create_all(bind=engine)


def seed():
    db = SessionLocal()
    try:
        users = [
            ("citizen", "Citizen@123", "CITIZEN"),
            ("admin", "Admin@123", "ADMIN"),
            ("rto", "Rto@12345", "RTO"),
        ]

        for username, password, role in users:
            if not db.query(User).filter(User.username == username).first():
                db.add(
                    User(
                        name=username.title(),
                        username=username,
                        password_hash=hash_password(password),
                        role=role,
                        status="ACTIVE",
                    )
                )

        db.commit()
        print("Development users seeded.")
    finally:
        db.close()


if __name__ == "__main__":
    seed()
