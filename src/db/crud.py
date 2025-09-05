import pandas as pd

from sqlalchemy.orm import Session
from sqlalchemy.orm import sessionmaker
from sqlalchemy import select, text

from . import engine
from .indice_repuesto_model import IndiceRepuesto

Session = sessionmaker(bind=engine)

# create
def df_to_sql(table: str, df: pd.DataFrame):
    with engine.begin() as connection:
        df.to_sql(table, con=connection, index=False, if_exists="append")


# delete
def delete_indice_repuesto(id: int):
    with Session() as session:
        with session.begin():
            repuesto = session.get(IndiceRepuesto, id)
            if repuesto:
                session.delete(repuesto)


# read
def read_all_repuestos():
    with Session() as session:
        return session.scalars(select(IndiceRepuesto)).all() # type: ignore        


def sql_to_df_by_type(table: str, tipo_repuesto: str) -> pd.DataFrame:
    with engine.begin() as connection:
        query = f"SELECT * FROM {table} WHERE TipoRepuesto = :tipo"
        return pd.read_sql_query(query, con=connection, params={"tipo":tipo_repuesto})


def sql_to_df(table: str):
    with engine.begin() as connection:
        return pd.read_sql_table(table, connection) 