from typing import Any

import pandas as pd
from sqlalchemy import select, ScalarResult

from src.config.enums import IndexTypeEnum
from . import SessionServices
from . import services_engine


# ---------------------------------   CREATE   --------------------------------- #
def df_to_db(table: str, df: pd.DataFrame):
    """
    Guarda un dataframe pasado por parámetro a services_data.db
    - table -> Nombre de la tabla a guardar.
    - df -> DataFrame con los datos.
    - if_exists -> funcion que se va a realizar cuando se introduzca un dato repetido (dejar en append).
    """
    with services_engine.begin() as connection:
        df.to_sql(table, con=connection, index=False, if_exists="append")


# ---------------------------------   DELETE   --------------------------------- #
class SericeDelete:
    @staticmethod
    def by_id(table, _id: int):
        """
        Elimina datos de una tabla de services_data.db a partir del id.
        - table -> ModelClass()
        - id -> PK
        """
        with SessionServices() as session:
            with session.begin():
                row = session.get(table, id)
                if row:
                    session.delete(row)


    @staticmethod
    def table(table: str):
        """
        Elimina una tabla dado el nombre de la misma en services_data.db
        """
        with SessionServices() as session:
            session.delete(table)
            session.commit()


# ---------------------------------   READ   --------------------------------- #

class ServiceRead:
    @staticmethod
    def all_scalar(table) -> ScalarResult[Any]:
        """
        Lee todos los datos de una tabla de services_data.db
        - table -> ModelClass()
        """
        with SessionServices() as session:
            return session.scalars(select(table)).all()
        
        
    @staticmethod
    def all_df(table) -> pd.DataFrame:
        """
            Hace una consulta a la base de datos de services_data.db,
            y lo devuelve en forma de dataframe.
            """
        query = select(table)
        return pd.read_sql_query(query, con=services_engine)


    @staticmethod
    def date(table) -> pd.DataFrame:
        """
        Lee la fecha de la columna FechaCompleta
        de cualquier tabla de services_data.db
        """
        query = select(table.FechaCompleta)
        return pd.read_sql_query(query, con=services_engine)
    
    
    @staticmethod
    def by_cabecera(table, cabecera: str) -> pd.DataFrame:
        """
            Hace un query a la base de datos de services_data.db,
            mediante la condicion de cabecera y lo devuelve en forma de dataframe.
            """
        query = select(table).where(table.Cabecera == cabecera)  # type: ignore
        return pd.read_sql_query(query, con=services_engine)
    
    
    @staticmethod
    def by_repuesto(table, tipo_repuesto: str) -> pd.DataFrame:
        """
            Hace un query a la base de datos de services_data.db,
            mediante la condicion de tipo_repuesto y lo devuelve en forma de dataframe.
            """
        query = select(table).where(table.TipoRepuesto == tipo_repuesto)  # type: ignore
        return pd.read_sql_query(query, con=services_engine)
    
    
    @staticmethod
    def by_rep_and_index(table, tipo_repuesto: str, tipo_indice: IndexTypeEnum) -> pd.DataFrame:
        query = select(table).where(
            table.TipoRepuesto == tipo_repuesto, table.TipoOperacion == tipo_indice  # type: ignore
        )
        return pd.read_sql_query(query, con=services_engine)


    @staticmethod
    def by_cabecera_and_rep(table, cabecera: str, tipo_repuesto: str) -> pd.DataFrame:
        query = select(table).where(
            table.Cabecera == cabecera, table.TipoRepuesto == tipo_repuesto  # type: ignore
        )
        return pd.read_sql_query(query, con=services_engine)


    @staticmethod
    def by_rep_and_tipo_rep(table, repuesto: str, tipo_rep: str) -> pd.DataFrame:
        query = select(table).where(
            table.Repuesto == repuesto, table.TipoRepuesto == tipo_rep  # type: ignore
        )
        return pd.read_sql_query(query, con=services_engine)


    @staticmethod
    def by_rep_and_tipo_rep_and_cabecera(table, repuesto: str, tipo_rep: str, cabecera: str) -> pd.DataFrame:
        query = select(table).where(
            table.Repuesto == repuesto, table.TipoRepuesto == tipo_rep, table.Cabecera == cabecera  # type: ignore
        )
        return pd.read_sql_query(query, con=services_engine)






        