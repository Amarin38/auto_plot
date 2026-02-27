from datetime import date
from typing import Optional, Any

import numpy as np
import streamlit as st
import pandas as pd
from pandas import DataFrame

from domain.entities.parque_movil import ParqueMovil, ParqueMovilFiltro
from infrastructure.repositories.parque_movil_repository import ParqueMovilRepository
from interfaces.viewmodel import ViewModel

@st.cache_data(ttl=3600, show_spinner="Consultando a la base de datos...", show_time=True)
def _fetch_base_dataframe(fecha_desde: date, fecha_hasta: date):
    repo = ParqueMovilRepository()
    entities = repo.get_by_args(fecha_desde, fecha_hasta)

    if not entities:
        return pd.DataFrame()

    rows = ((
        e.id, e.FechaParqueMovil, e.Linea, e.Interno, e.Dominio, e.Asientos,
        e.Año, e.ChasisMarca, e.ChasisModelo, e.ChasisNum, e.MotorMarca,
        e.MotorModelo, e.MotorNum, e.Carroceria) for e in entities)

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

    return pd.DataFrame(df.astype({
            "Linea": "category",
            "Interno": "uint16",
            "Dominio": "string[pyarrow]",
            "Asientos": "category",
            "Año": "uint16",
            "ChasisMarca": "category",
            "ChasisModelo": "category",
            "ChasisNum": "string[pyarrow]",
            "MotorMarca": "category",
            "MotorModelo": "category",
            "MotorNum": "string[pyarrow]",
            "Carroceria": "category",
        })
    )


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
        _fetch_base_dataframe.clear()


    def get_df(self) -> pd.DataFrame:
        entities = self.repo.get_all()
        return self.get_data(entities)

    @staticmethod
    def get_by_args(fecha_desde: date, fecha_hasta: date, parque: ParqueMovilFiltro) -> Optional[Any]:
        df_base = _fetch_base_dataframe(fecha_desde, fecha_hasta)

        if df_base.empty:
            return pd.DataFrame()

        mask = np.ones(len(df_base), dtype=bool)

        if parque.Linea:
           mask &= df_base["Linea"] == int(parque.Linea)

        if parque.Interno:
            mask &= df_base["Interno"] == int(parque.Interno)

        if parque.Dominio:
            mask &= df_base["Dominio"].str.startswith(parque.Dominio)

        if parque.ChasisMarca:
            mask &= df_base["ChasisMarca"].isin(parque.ChasisMarca)

        if parque.ChasisModelo:
            mask &= df_base["ChasisModelo"].isin(parque.ChasisModelo)

        if parque.MotorMarca:
            mask &= df_base["MotorMarca"].isin(parque.MotorMarca)

        if parque.MotorModelo:
            mask &= df_base["MotorModelo"].isin(parque.MotorModelo)

        if parque.Carroceria:
            mask &= df_base["Carroceria"].isin(parque.Carroceria)

        return df_base[mask]


    @staticmethod
    def get_data(entities) -> DataFrame:
        return pd.DataFrame([
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
        ])