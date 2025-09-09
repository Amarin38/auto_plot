import pandas as pd

from sqlalchemy.orm import Session
from sqlalchemy.orm import sessionmaker
from sqlalchemy import select

from . import engine

Session = sessionmaker(bind=engine)

def df_to_sql(table: str, df: pd.DataFrame):
    with engine.begin() as connection:
        df.to_sql(table, con=connection, index=False, if_exists="append")


# ----------------------------------------------------
def delete_by_id(table, id: int):
    with Session() as session:
        with session.begin():
            row = session.get(table, id)
            if row:
                session.delete(row)


def delete_table(table: str):
    with Session() as session:
        session.delete(table)
        session.commit()


# ----------------------------------------------------
def read_all(table):
    with Session() as session:
        return session.scalars(select(table)).all()  


def read_date(table):
    query = select(table.FechaCompleta)
    return pd.read_sql_query(query, con=engine)
        

def sql_to_df_by_type(table, tipo_repuesto: str) -> pd.DataFrame:
    query = select(table).where(table.TipoRepuesto == tipo_repuesto)
    return pd.read_sql_query(query, con=engine)


def sql_to_df(table: str):
    with engine.begin() as connection:
        return pd.read_sql_table(table, connection) 
    