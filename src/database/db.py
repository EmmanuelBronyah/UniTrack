from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
from platformdirs import user_data_dir
from pathlib import Path
import shutil
import sys

load_dotenv()


APP_NAME, APP_AUTHOR = "UniTrack", "UniTrack"


def create_db_path():
    """
    Determines the database path for the user.
    If the database doesn't exist, it copies the prefilled one.
    Works in both dev and PyInstaller .exe environments.
    """
    # User's local data directory (e.g., AppData\Local\UniTrack)
    data_dir = Path(user_data_dir(APP_NAME, APP_AUTHOR))
    data_dir.mkdir(parents=True, exist_ok=True)
    db_path = data_dir / "unitrack.db"

    if not db_path.exists():
        # Determine where the bundled data is
        if getattr(sys, "frozen", False):  # Running from PyInstaller .exe
            base_dir = Path(sys._MEIPASS)
        else:
            base_dir = Path(__file__).resolve().parent.parent

        bundled_db = base_dir / "data" / "unitrack.db"

        if bundled_db.exists():
            shutil.copy(bundled_db, db_path)
        else:
            pass

    return f"sqlite:///{db_path.as_posix()}"


db_url = create_db_path()


engine = create_engine(db_url, connect_args={"check_same_thread": False}, echo=False)

Base = declarative_base()

from src.database import models

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
