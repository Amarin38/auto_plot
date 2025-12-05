import datetime
from typing import List, Optional

import pandas as pd

from domain.entities.parque_movil import ParqueMovil
from infrastructure.repositories.parque_movil_repository import ParqueMovilRepository
from interfaces.viewmodel import ViewModel


class ParqueMovilVM(ViewModel):
    def __init__(self) -> None:
        self.repo = ParqueMovilRepository()

    def save_df(self, df) -> None:
        entities = []

        df["FechaParqueMovil"] = pd.to_datetime(df["FechaParqueMovil"])

        for _, row in df.iterrows():
            entity = ParqueMovil(
                id                  = None,
                FechaParqueMovil    = row['FechaParqueMovil'],
                Linea               = row['Linea'],
                Interno             = row['Interno'],
                Dominio             = row['Dominio'],
                Asientos            = row['Asientos'],
                Año                 = row['Año'],
                ChasisMarca         = row['ChasisMarca'],
                ChasisModelo        = row['ChasisModelo'],
                ChasisNum           = row['ChasisNum'],
                MotorMarca          = row['MotorMarca'],
                MotorModelo         = row['MotorModelo'],
                MotorNum            = row['MotorNum'],
                Carroceria          = row['Carroceria'],
            )
            entities.append(entity)

        self.repo.insert_many(entities)

    def get_df(self) -> pd.DataFrame:
        entities = self.repo.get_all()

        data = [
            {
                "id"                    : e.id,
                "FechaParqueMovil"      : e.FechaParqueMovil,
                "Linea"                 : e.Linea,
                "Interno"               : e.Interno,
                "Dominio"               : e.Dominio,
                "Asientos"              : e.Asientos,
                "Año"                   : e.Año,
                "ChasisMarca"           : e.ChasisMarca,
                "ChasisModelo"          : e.ChasisModelo,
                "ChasisNum"             : e.ChasisNum,
                "MotorMarca"            : e.MotorMarca,
                "MotorModelo"           : e.MotorModelo,
                "MotorNum"              : e.MotorNum,
                "Carroceria"            : e.Carroceria,
            }
            for e in entities
        ]

        return pd.DataFrame(data)

    def get_by_args(self, fecha_inicio: Optional[datetime.date], fecha_fin: Optional[datetime.date],
                          linea: Optional[int], interno: Optional[int], dominio: Optional[str], series: Optional[List[str]]) -> pd.DataFrame:

        entities = self.repo.get_by_args(fecha_inicio, fecha_fin, linea, interno, dominio, series)

        data = [
            {
                "id": e.id,
                "FechaParqueMovil": e.FechaParqueMovil,
                "Linea": e.Linea,
                "Interno": e.Interno,
                "Dominio": e.Dominio,
                "Asientos": e.Asientos,
                "Año": e.Año,
                "ChasisMarca": e.ChasisMarca,
                "ChasisModelo": e.ChasisModelo,
                "ChasisNum": e.ChasisNum,
                "MotorMarca": e.MotorMarca,
                "MotorModelo": e.MotorModelo,
                "MotorNum": e.MotorNum,
                "Carroceria": e.Carroceria,
            }
            for e in entities
        ]

        return pd.DataFrame(data)