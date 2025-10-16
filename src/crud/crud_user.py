from sqlalchemy.orm import Session
from src.database.models import User
from src.security import hash_password, verify_password


def create_user(db: Session, service_number: str, username: str, password: str) -> User:
    user = User(
        service_number=service_number,
        username=username,
        password=hash_password(password),
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    return user


def login_user(db: Session, username: str, password: str) -> User | None:
    user = db.query(User).filter(User.username == username).first()

    if user:
        hashed_password = user.password
        is_valid_password = verify_password(password, hashed_password)
        if is_valid_password:
            return user
        return None

    return None
