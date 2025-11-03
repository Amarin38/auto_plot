import json
from typing import Union, Dict, Any

import pandas as pd
from sqlalchemy import select, func

from src.config.constants import JSON_PATH
from src.db_data.models.common_model.json_config_model import JSONConfigModel
from . import SessionCommon
from . import common_engine


# ---------------------------------   CREATE   --------------------------------- #
def df_to_db(table: str, df: pd.DataFrame):
    """
    Guarda un dataframe pasado por parámetro a common_data.db
    - table -> Nombre de la tabla a guardar.
    - df -> DataFrame con los datos.
    - if_exists -> funcion que se va a realizar cuando se introduzca un dato repetido (dejar en append).
    """
    with common_engine.begin() as connection:
        df.to_sql(table, con=connection, index=False, if_exists="append")


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


class CommonDelete:
    @staticmethod
    def by_id(table, _id: int):
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


    @staticmethod
    def table(table: str):
        """
        Elimina una tabla dado el nombre de la misma en common_data.db
        """
        with SessionCommon() as session:
            session.delete(table)
            session.commit()


class CommonRead:
    @staticmethod
    def all_scalar(table):
        """
        Lee todos los datos de una tabla de common_data.db
        - table -> ModelClass()
        """
        with SessionCommon() as session:
            return session.scalars(select(table)).all()


    @staticmethod
    def all_df(table):
        """
        Hace una consulta a la base de datos de common_data.db y lo devuelve en forma de dataframe.
        """
        query = select(table)
        return pd.read_sql_query(query, con=common_engine)


    @staticmethod
    def by_tipo_repuesto(table, tipo_repuesto: str) -> pd.DataFrame:
        """
        Hace un query a la base de datos de common_data.db
        mediante la condicion de tipo_repuesto y lo devuelve en forma de dataframe.
        """
        query = select(table).where(table.TipoRepuesto == tipo_repuesto)  # type: ignore
        return pd.read_sql_query(query, con=common_engine)


    # ---------------------------------   DATE  --------------------------------- #
    @staticmethod
    def min_date(table) -> str:
        with SessionCommon() as session:
            return session.query(func.min(table.FechaIngreso)).scalar()


    @staticmethod
    def max_date(table) -> str:
        with SessionCommon() as session:
            return session.query(func.max(table.FechaIngreso)).scalar()


    # ---------------------------------   READ JSON   --------------------------------- #
    @staticmethod
    def pk_json_config(nombre_dato: str) -> int:
        """
        Devuelve la PK de la tabla JSONConfig a partir del nombre.
        """
        with SessionCommon() as session:
            stmnt = select(JSONConfigModel).where(JSONConfigModel.nombre == nombre_dato)
            return session.scalar(stmnt).id  # type: ignore


    @staticmethod
    def json_config(identificador: Union[str, int]) -> Dict[str, Any]:
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

            return session.scalar(stmnt).data  # type: ignore

    