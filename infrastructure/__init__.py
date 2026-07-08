import streamlit as st
from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker

from config.constants_common import DB_PATH_SQLITE, DB_PATH_POSTGRES


@st.cache_resource
def get_db_engine_sqlite():
    return create_engine(DB_PATH_SQLITE, echo=False)


@st.cache_resource
def get_db_engine_postgres():
    return create_engine(
        DB_PATH_POSTGRES,
        pool_pre_put=True,
        echo=False,
        connect_args={'options': '-csearch_path=estadisticas,datos'}
    )


@st.cache_resource
def get_db_session(_engine):
    return sessionmaker(bind=_engine)


# SQLITE
dbbase_sqlite       = declarative_base()
db_engine_sqlite    = get_db_engine_sqlite()
session_sqlite_db   = get_db_session(db_engine_sqlite)


# POSTGRES
schema_estadisticas = MetaData(schema="estadisticas")
schema_datos        = MetaData(schema="datos")

dbbase_postrgres        = declarative_base(metadata=schema_datos)
db_engine_postgres      = get_db_engine_postgres()
session_postgres_db     = get_db_session(db_engine_postgres)



