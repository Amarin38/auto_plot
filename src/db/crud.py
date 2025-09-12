import json
import pandas as pd
from typing import Literal, Union

from sqlalchemy import select
from sqlalchemy.orm import Session
from sqlalchemy.orm import sessionmaker

from src.db.models.json_config_model import JSONConfigModel
from src.config.constants import JSON_PATH

from . import engine

Session = sessionmaker(bind=engine)

# ----------------------------------------------------

def df_to_sql(table: str, df: pd.DataFrame, if_exists: Literal["fail", "replace", "append"]):
    with engine.begin() as connection:
        df.to_sql(table, con=connection, index=False, if_exists=if_exists)


def json_to_sql(config_name: str, data):
    from src.db.models.json_config_model import JSONConfigModel

    with Session() as session:
        json_file = JSONConfigModel(nombre=config_name, data=data)
        
        session.add(json_file)
        session.commit()
        

def store_json_file(file_name:str, ):
    with open(f"{JSON_PATH}/{file_name}.json", encoding="UTF-8", mode="r") as f:
        data = json.load(f)
        json_to_sql(file_name, data)

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


def get_pk_json_config(nombre_dato: str) -> int:
    with Session() as session:
        stmnt = select(JSONConfigModel).where(JSONConfigModel.nombre == nombre_dato)
        return session.scalar(stmnt).id # type: ignore


def read_json_config(identificador: Union[str, int]):
    with Session() as session:
        if isinstance(identificador, str):
            stmnt = select(JSONConfigModel).where(JSONConfigModel.nombre == identificador)
        elif isinstance(identificador, int):
            stmnt = select(JSONConfigModel).where(JSONConfigModel.id == identificador)

        return session.scalar(stmnt).data # type: ignore
        
        