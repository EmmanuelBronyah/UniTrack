from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
from platformdirs import user_data_dir
from pathlib import Path


load_dotenv()


APP_NAME, APP_AUTHOR = "UniTrack", "UniTrack"


def create_db_path():
    data_dir = Path(user_data_dir(APP_NAME, APP_AUTHOR))
    data_dir.mkdir(parents=True, exist_ok=True)
    db_path = data_dir / "unitrack.db"

    return f"sqlite:///{db_path.as_posix()}"


db_url = create_db_path()


engine = create_engine(db_url, connect_args={"check_same_thread": False}, echo=False)

Base = declarative_base()

from src.database import models

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
