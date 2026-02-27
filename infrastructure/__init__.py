import streamlit as st
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker

from config.constants_common import DB_PATH

DBBase = declarative_base()

@st.cache_resource
def get_db_engine():
    return create_engine(DB_PATH, echo=False)

@st.cache_resource
def get_db_session(_engine):
    return sessionmaker(bind=_engine)

db_engine = get_db_engine()
SessionDB = get_db_session(db_engine)




