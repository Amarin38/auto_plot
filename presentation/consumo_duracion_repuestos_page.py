from typing import Any, Dict

import pandas as pd
import streamlit as st

from config.constants_common import DURACION_REPUESTO_KEY
from config.enums import CambiosEnum
from config.enums_colors import CustomMetricColorsEnum
from config.constants_views import PAG_DURACION, DURACION_TAB_BOX_HEIGHT, SELECT_BOX_HEIGHT
from infrastructure.unit_of_work import SQLAlchemyUnitOfWork
from viewmodels.consumo.duracion_rep.vm import DuracionRepuestosVM
from viewmodels.consumo.duracion_rep.plotter import DuracionRepuestosPlotter
from utils.exception_utils import execute_safely
from presentation.streamlit_components import SelectBoxComponents, OtherComponents


@st.cache_data(ttl=200, show_spinner=False)
def _cargar_datos(repuesto) -> Dict[str, Any]:
    vm = DuracionRepuestosVM(uow=SQLAlchemyUnitOfWork())

    duracion = vm.get_df_by_repuesto(repuesto)
    distribucion = vm.get_distribucion_df_by_repuesto(repuesto)

    return {
        "duracion": duracion,
        "distribucion": distribucion,
        "2015": calcular_sin_cambios(duracion, "2015"),
        "2016": calcular_sin_cambios(duracion, "2016"),
        "2017": calcular_sin_cambios(duracion, "2017")
    }


@execute_safely
def calcular_sin_cambios(df_duracion: pd.DataFrame, year_str: str) -> Any:
    year = pd.to_datetime(year_str, errors="coerce")
    df_duracion["FechaCambio"] = pd.to_datetime(df_duracion["FechaCambio"], errors="coerce")

    df_year = df_duracion.loc[
        (df_duracion["FechaCambio"].dt.year == year.year) &
        (df_duracion["Cambio"] == 0),
        ["Patente"]
    ]

    df_sin_cambios = (
        df_duracion
        .merge(df_year, on="Patente", how="inner")
        .loc[
            (df_duracion["Cambio"] == 1) &
            (df_duracion["FechaCambio"] == pd.Timestamp("2025-10-28"))
            ]
    )

    return df_sin_cambios.count().iat[0]


@execute_safely
def duracion_repuestos():
    select = SelectBoxComponents()
    components = OtherComponents()

    st.title(PAG_DURACION)

    aux1, filas_col, rep_col, aux3 = st.columns((0.8, 0.5, 0.75, 0.8))

    select_rep = select.select_box_repuesto(rep_col, DURACION_REPUESTO_KEY)

    with filas_col.container(height=SELECT_BOX_HEIGHT, vertical_alignment='center'):
        select_filas = st.selectbox("Seleccione la cantidad de cambios:", CambiosEnum)

    match select_filas:
        case CambiosEnum._4_CAMBIOS: filas = 2
        case CambiosEnum._6_CAMBIOS: filas = 3
        case _: filas = 1

    with st.container(height=DURACION_TAB_BOX_HEIGHT):
        if select_rep:
            with st.spinner("Cargando duraciones..."):
                datos = _cargar_datos(select_rep)

                df_duracion     = datos["duracion"]
                df_distribucion = datos["distribucion"]
                d_2015 = datos["2015"]
                d_2016 = datos["2016"]
                d_2017 = datos["2017"]

            if len(df_duracion) and len(df_distribucion):
                fig = DuracionRepuestosPlotter(df_duracion, df_distribucion, filas).create_plot()

                _, col_2015, col_2016, col_2017, _ = st.columns((1, 1, 1, 1, 1))

                if any([d_2015, d_2016, d_2017]):
                    components.custom_metric(
                        col_2015,
                        "Sin cambios 2015",
                        d_2015,
                        CustomMetricColorsEnum.ROJO,
                        CustomMetricColorsEnum.ROJO
                    )

                    components.custom_metric(
                        col_2016,
                        "Sin cambios 2016",
                        d_2016,
                        CustomMetricColorsEnum.AZUL,
                        CustomMetricColorsEnum.AZUL
                    )

                    components.custom_metric(
                        col_2017,
                        "Sin cambios 2017",
                        d_2017,
                        CustomMetricColorsEnum.AMARILLO,
                        CustomMetricColorsEnum.AMARILLO
                    )

                st.plotly_chart(fig)

