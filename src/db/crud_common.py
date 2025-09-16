import json
import pandas as pd
from typing import Literal, Union, Dict, Any

from sqlalchemy import select

from src.config.constants import JSON_PATH

from src.db.models.json_config_model import JSONConfigModel

from . import common_engine
from . import SessionCommon



# ---------------------------------   CREATE   --------------------------------- #
def df_to_db(table: str, df: pd.DataFrame, if_exists: Literal["fail", "replace", "append"]):
    """
    Guarda un dataframe pasado por parámetro a common_data.db
    - table -> Nombre de la tabla a guardar.
    - df -> DataFrame con los datos.
    - if_exists -> funcion que se va a realizar cuando se introduzca un dato repetido (dejar en append).
    """
    with common_engine.begin() as connection:
        df.to_sql(table, con=connection, index=False, if_exists=if_exists)


def json_to_sql(config_name: str, data):
    """
    Guarda un archivo JSON en common_data.db a partir de su nombre.
    - config_name -> Nombre de la configuracion a guardar.
    - data -> Datos del json.
    """
    with SessionCommon() as session:
        json_file = JSONConfigModel(nombre=config_name, data=data)
        
        session.add(json_file)
        session.commit()
    

def store_json_file(self, file_name: str):
    """
    Busca el archivo en el directorio actual 
    y lo guarda en la base de datos llamando a json_to_sql()
    """
    with open(f"{JSON_PATH}/{file_name}.json", encoding="UTF-8", mode="r") as f:
        data = json.load(f)
        self.json_to_sql(file_name, data)


# ---------------------------------   DELETE   --------------------------------- #
def delete_by_id(table, id: int):
    """
    Elimina datos de una tabla de common_data.db a partir del id.
    - table -> ModelClass()
    - id -> PK
    """
    with SessionCommon() as session:
        with session.begin():
            row = session.get(table, id)
            if row:
                session.delete(row)


def delete_table(table: str):
    """
    Elimina una tabla dado el nombre de la misma en common_data.db
    """
    with SessionCommon() as session:
        session.delete(table)
        session.commit()


# ---------------------------------   READ   --------------------------------- #
def read_all(table):
    """
    Lee todos los datos de una tabla de common_data.db
    - table -> ModelClass()
    """
    with SessionCommon() as session:
        return session.scalars(select(table)).all()  


def sql_to_df_by_type(table, tipo_repuesto: str) -> pd.DataFrame:
    """
    Hace un query a la base de datos de common_data.db\n 
    mediante la condicion de tipo_repuesto y lo devuelve en forma de dataframe.
    """
    query = select(table).where(table.TipoRepuesto == tipo_repuesto)
    return pd.read_sql_query(query, con=common_engine)


def db_to_df(table: str):
    """
    Hace una consulta a la base de datos de common_data.db y lo devuelve en forma de dataframe.    
    """
    with common_engine.begin() as connection:
        return pd.read_sql_table(table, connection) 
    

# ---------------------------------   READ JSON   --------------------------------- #
def get_pk_json_config(nombre_dato: str) -> int:
    """
    Devuelve la PK de la tabla JSONConfig a partir del nombre.
    """
    with SessionCommon() as session:
        stmnt = select(JSONConfigModel).where(JSONConfigModel.nombre == nombre_dato)
        return session.scalar(stmnt).id # type: ignore


def read_json_config(identificador: Union[str, int]) -> Dict[str, Any]:
    """
    Lee los datos de la tabla JSONConfig a partir de un identificador.
    - INT -> PK
    - STR -> Nombre de la config. de JSON
    """
    with SessionCommon() as session:
        if isinstance(identificador, str):
            stmnt = select(JSONConfigModel).where(JSONConfigModel.nombre == identificador)
        elif isinstance(identificador, int):
            stmnt = select(JSONConfigModel).where(JSONConfigModel.id == identificador)

        return session.scalar(stmnt).data # type: ignore
    