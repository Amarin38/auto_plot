from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker

from config.constants import DB_PATH

db_engine = create_engine(DB_PATH, echo=False)

SessionDB = sessionmaker(bind=db_engine)

DBBase = declarative_base()



