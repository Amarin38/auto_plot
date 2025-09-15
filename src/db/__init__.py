from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker

from src.config.constants import COMMON_DB_PATH, SERV_DB_PATH

common_engine = create_engine(f"sqlite:///{COMMON_DB_PATH}", echo=True)
services_engine = create_engine(f"sqlite:///{SERV_DB_PATH}", echo=True)

SessionCommon = sessionmaker(bind=common_engine)
SessionServices = sessionmaker(bind=services_engine)

CommonBase = declarative_base()
ServicesBase = declarative_base()




