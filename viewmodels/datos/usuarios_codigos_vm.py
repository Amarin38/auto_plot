import pandas as pd
from pandas import DataFrame

from domain.entities.datos_usuarios_codigos import UsuariosCodigos
from infrastructure.unit_of_work import SQLAlchemyUnitOfWork


class UsuariosCodigosVM:
    def __init__(self, uow: SQLAlchemyUnitOfWork = SQLAlchemyUnitOfWork()) -> None:
        self.uow = uow

    def save_df(self, df) -> None:
        entities = [
            UsuariosCodigos(
                id                      = None,
                UsuariosAntiguos        = row['UsuariosAntiguos'],
                UsuariosNuevos          = row['UsuariosNuevos'],
                NombresAntiguos         = row['NombresAntiguos'],
                NombresNuevos           = row['NombresNuevos'],
            ) for index, row in df.iterrows()
        ]

        with self.uow as uow:
            uow.usuarios_codigos.insert_many(entities)


    def get_df(self) -> pd.DataFrame:
        with self.uow as uow:
            entities = uow.usuarios_codigos.get_all()
            return self.get_data(entities) if entities else pd.DataFrame()


    def get_df_by_usuario_antiguo(self, usuario_antiguo: str) -> pd.DataFrame:
        with self.uow as uow:
            entities = uow.usuarios_codigos.get_by_usuario_antiguo(usuario_antiguo)
            return self.get_data(entities) if entities else pd.DataFrame()


    def get_df_by_usuario_nuevo(self, usuario_nuevo: str) -> pd.DataFrame:
        with self.uow as uow:
            entities = uow.usuarios_codigos.get_by_usuario_nuevo(usuario_nuevo)
            return self.get_data(entities) if entities else pd.DataFrame()


    @staticmethod
    def get_data(entities) -> DataFrame:
        return pd.DataFrame([
                {
                    "id"                : e.id,
                    "UsuariosAntiguos"  : e.UsuariosAntiguos,
                    "UsuariosNuevos"    : e.UsuariosNuevos,
                    "NombresAntiguos"   : e.NombresAntiguos,
                    "NombresNuevos"     : e.NombresNuevos,
                }
                for e in entities
            ])