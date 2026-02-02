from datetime import date
from typing import Optional, Any

import numpy as np
import streamlit as st
import pandas as pd

from domain.entities.parque_movil import ParqueMovil, ParqueMovilFiltro
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

    @staticmethod
    # @st.cache_data
    def get_by_args(fecha_desde: date, fecha_hasta: date, parque: ParqueMovilFiltro) -> Optional[Any]:
        entities = ParqueMovilRepository().get_by_args(fecha_desde, fecha_hasta)

        if not entities:
            return None

        rows = (
            (
                e.id, e.FechaParqueMovil, e.Linea, e.Interno, e.Dominio, e.Asientos,
                e.Año, e.ChasisMarca, e.ChasisModelo, e.ChasisNum, e.MotorMarca,
                e.MotorModelo, e.MotorNum, e.Carroceria
            ) for e in entities
        )

        cols = ("id", "FechaParqueMovil", "Linea", "Interno", "Dominio", "Asientos",
                "Año", "ChasisMarca", "ChasisModelo", "ChasisNum", "MotorMarca",
                "MotorModelo", "MotorNum", "Carroceria")

        df = pd.DataFrame.from_records(rows, columns=cols)

        df["Linea"] = df["Linea"].fillna(0)
        df["Interno"] = df["Interno"].fillna(0)
        df["Dominio"] = df["Dominio"].fillna("")
        df["Asientos"] = df["Asientos"].fillna(0)
        df["Año"] = df["Año"].fillna(0)
        df["ChasisMarca"] = df["ChasisMarca"].fillna("")
        df["ChasisModelo"] = df["ChasisModelo"].fillna("")
        df["ChasisNum"] = df["ChasisNum"].fillna("")
        df["MotorMarca"] = df["MotorMarca"].fillna("")
        df["MotorModelo"] = df["MotorModelo"].fillna("")
        df["MotorNum"] = df["MotorNum"].fillna("")
        df["Carroceria"] = df["Carroceria"].fillna("")

        data_filtrado = df.astype({
            "Linea":"category",
            "Interno":"uint16",
            "Dominio":"string[pyarrow]",
            "Asientos":"category",
            "Año":"uint16",
            "ChasisMarca":"category",
            "ChasisModelo":"category",
            "ChasisNum":"string[pyarrow]",
            "MotorMarca":"category",
            "MotorModelo":"category",
            "MotorNum":"string[pyarrow]",
            "Carroceria":"category",
        })

        mask = np.ones(len(df), dtype=bool)

        if parque.Linea:
           mask &= data_filtrado["Linea"] == int(parque.Linea)

        if parque.Interno:
            mask &= data_filtrado["Interno"] == int(parque.Interno)

        if parque.Dominio:
            mask &= data_filtrado["Dominio"].str.startswith(parque.Dominio)

        if parque.ChasisMarca:
            mask &= data_filtrado["ChasisMarca"].isin(parque.ChasisMarca)

        if parque.ChasisModelo:
            mask &= data_filtrado["ChasisModelo"].isin(parque.ChasisModelo)

        if parque.MotorMarca:
            mask &= data_filtrado["MotorMarca"].isin(parque.MotorMarca)

        if parque.MotorModelo:
            mask &= data_filtrado["MotorModelo"].isin(parque.MotorModelo)

        if parque.Carroceria:
            mask &= data_filtrado["Carroceria"].isin(parque.Carroceria)

        return data_filtrado[mask]
