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


def get_user(db: Session):
    user = db.query(User).first()
    user_dict = user.__dict__
    return user_dict


def update_user(db: Session, user: dict):
    db_user = db.query(User).first()
    db_hash_password = db_user.password

    current_password = user["current_password"]
    new_password = user["new_password"]
    username = user["username"]

    is_valid_password = verify_password(current_password, db_hash_password)

    if is_valid_password:
        db_user.password = hash_password(new_password)
        db_user.username = username
        return True

    return False
