from datetime import date

import streamlit as st
import pandas as pd
from pandas import DataFrame

from config.constants_common import PARQUE_MOVIL_COLS, PARQUE_MOVIL_COLS_TYPE
from domain.entities.datos.parque_movil import ParqueMovil
from infrastructure.unit_of_work import SQLAlchemyUnitOfWork


@st.cache_data(ttl=3600, show_spinner="Consultando a la base de datos...", show_time=True)
def _fetch_base_dataframe(fecha_desde: date, fecha_hasta: date, _uow: SQLAlchemyUnitOfWork):
    entities = _uow.parque_movil.get_by_args(fecha_desde, fecha_hasta)

    if not entities:
        return pd.DataFrame()

    rows = ((
        e.id, e.FechaParqueMovil, e.Linea, e.Interno, e.Dominio, e.Asientos,
        e.Año, e.ChasisMarca, e.ChasisModelo, e.ChasisNum, e.MotorMarca,
        e.MotorModelo, e.MotorNum, e.Carroceria
    ) for e in entities)

    df = pd.DataFrame.from_records(rows, columns=PARQUE_MOVIL_COLS)
    valores_na = {"Linea":0, "Interno":0, "Dominio":"", "Asientos":0, "Año":0,
                  "ChasisMarca":"", "ChasisModelo":"", "ChasisNum":"",
                  "MotorMarca":"", "MotorModelo":"", "MotorNum":"", "Carroceria":""}

    df = df.fillna(value=valores_na).astype(PARQUE_MOVIL_COLS_TYPE)
    return df


class ParqueMovilVM:
    def __init__(self, uow: SQLAlchemyUnitOfWork = SQLAlchemyUnitOfWork()) -> None:
        self.uow = uow

    def save_df(self, df) -> None:
        df["FechaParqueMovil"] = pd.to_datetime(df["FechaParqueMovil"])

        entities = [
            ParqueMovil(
                id               = None,
                FechaParqueMovil = row['FechaParqueMovil'],
                Linea            = row['Linea'],
                Interno          = row['Interno'],
                Dominio          = row['Dominio'],
                Asientos         = row['Asientos'],
                Año              = row['Año'],
                Fecha0KM         = row['Fecha0KM'],
                ChasisMarca      = row['ChasisMarca'],
                ChasisModelo     = row['ChasisModelo'],
                ChasisNum        = row['ChasisNum'],
                MotorMarca       = row['MotorMarca'],
                MotorModelo      = row['MotorModelo'],
                MotorNum         = row['MotorNum'],
                Carroceria       = row['Carroceria'],
            ) for _, row in df.iterrows()
        ]

        with self.uow as uow:
            uow.parque_movil.insert_many(entities)
            _fetch_base_dataframe.clear()


    def get_df(self) -> pd.DataFrame:
        with self.uow as uow:
            entities = uow.parque_movil.get_all()
            return self.get_data(entities) if entities else pd.DataFrame()


    def get_by_fechas(self, fecha_desde: date, fecha_hasta: date) -> pd.DataFrame:
        with self.uow as uow:
            df_base = _fetch_base_dataframe(fecha_desde, fecha_hasta, uow)

        if df_base.empty:
            return pd.DataFrame()

        return df_base


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
                "Fecha0KM"              : e.Fecha0KM,
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