from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase

from src.config.constants import DB_PATH

engine = create_engine(f"sqlite:///{DB_PATH}", echo=True)

class Base(DeclarativeBase):
    pass







