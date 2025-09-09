import pandas as pd

from sqlalchemy.orm import Session
from sqlalchemy.orm import sessionmaker
from sqlalchemy import select

from . import engine

Session = sessionmaker(bind=engine)

# create
def df_to_sql(table: str, df: pd.DataFrame):
    with engine.begin() as connection:
        df.to_sql(table, con=connection, index=False, if_exists="append")


# delete
def delete_by_id(table, id: int):
    with Session() as session:
        with session.begin():
            row = session.get(table, id)
            if row:
                session.delete(row)


# read
def read_all(table):
    with Session() as session:
        return session.scalars(select(table)).all() # type: ignore        


def read_date(table):
    with engine.begin() as connection:
        query = f"SELECT FechaCompleta FROM {table}"
        return pd.read_sql_query(query, con=connection)
        

def sql_to_df_by_type(table: str, tipo_repuesto: str) -> pd.DataFrame:
    with engine.begin() as connection:
        query = f"SELECT * FROM {table} WHERE TipoRepuesto = :tipo"
        return pd.read_sql_query(query, con=connection, params={"tipo":tipo_repuesto})


def sql_to_df(table: str):
    with engine.begin() as connection:
        return pd.read_sql_table(table, connection) 
    