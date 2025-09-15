import pandas as pd
from typing import Literal

from sqlalchemy import select

from . import services_engine
from . import SessionServices


class CRUDServices:
    # ---------------------------------   CREATE   --------------------------------- #
    @staticmethod
    def df_to_db(table: str, df: pd.DataFrame, if_exists: Literal["fail", "replace", "append"]):
        """
        Guarda un dataframe pasado por parámetro a services_data.db
        - table -> Nombre de la tabla a guardar.
        - df -> DataFrame con los datos.
        - if_exists -> funcion que se va a realizar cuando se introduzca un dato repetido (dejar en append).
        """
        with services_engine.begin() as connection:
            df.to_sql(table, con=connection, index=False, if_exists=if_exists)


    # ---------------------------------   DELETE   --------------------------------- #
    @staticmethod
    def delete_by_id(table, id: int):
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
    def delete_table(table: str):
        """
        Elimina una tabla dado el nombre de la misma en services_data.db
        """
        with SessionServices() as session:
            session.delete(table)
            session.commit()


    # ---------------------------------   READ   --------------------------------- #
    @staticmethod
    def read_all(table):
        """
        Lee todos los datos de una tabla de services_data.db
        - table -> ModelClass()
        """
        with SessionServices() as session:
            return session.scalars(select(table)).all()  


    @staticmethod
    def read_date(table):
        """
        Lee la fecha de la columna FechaCompleta
        de cualquier tabla de services_data.db
        """
        query = select(table.FechaCompleta)
        return pd.read_sql_query(query, con=services_engine)
            

    @staticmethod
    def sql_to_df_by_type(table, tipo_repuesto: str) -> pd.DataFrame:
        """
        Hace un query a la base de datos de services_data.db\n 
        mediante la condicion de tipo_repuesto y lo devuelve en forma de dataframe.
        """
        query = select(table).where(table.TipoRepuesto == tipo_repuesto)
        return pd.read_sql_query(query, con=services_engine)


    @staticmethod
    def db_to_df(table: str):
        """
        Hace una consulta a la base de datos de services_data.db y lo devuelve en forma de dataframe.    
        """
        with services_engine.begin() as connection:
            return pd.read_sql_table(table, connection) 





        