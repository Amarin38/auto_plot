from typing import Any

import pandas as pd
import streamlit as st

from config.enums_colors import CustomMetricColorsEnum
from config.constants_views import PAG_DURACION, DURACION_TAB_BOX_HEIGHT, SELECT_BOX_HEIGHT
from utils.common_utils import CommonUtils
from viewmodels.consumo.duracion_rep.distri_normal_vm import DistribucionNormalVM
from viewmodels.consumo.duracion_rep.duracion_vm import DuracionRepuestosVM
from viewmodels.consumo.duracion_rep.plotter import DuracionRepuestosPlotter
from utils.exception_utils import execute_safely
from presentation.streamlit_components import SelectBoxComponents, OtherComponents


@st.cache_data(ttl=200, show_spinner=False)
def _cargar_datos(repuesto):
    duracion = DuracionRepuestosVM().get_df_by_repuesto(repuesto)
    distribucion = DistribucionNormalVM().get_df_by_repuesto(repuesto)

    return (duracion, distribucion,
            calcular_sin_cambios(duracion, "2015"),
            calcular_sin_cambios(duracion, "2016"),
            calcular_sin_cambios(duracion, "2017"))


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

    select_rep = select.select_box_repuesto(rep_col, "DURACION_REPUESTO_GENERAL")

    with filas_col.container(height=SELECT_BOX_HEIGHT, vertical_alignment='center'):
        select_filas = st.selectbox("Seleccione la cantidad de cambios:", ["2 cambios", "4 cambios", "6 cambios"])

    if select_filas == "4 cambios": filas = 2
    elif select_filas == "6 cambios": filas = 3
    else: filas = 1

    with st.container(height=DURACION_TAB_BOX_HEIGHT):
        if select_rep:
            with st.spinner("Cargando duraciones..."):
                df_duracion, df_distribucion, cambios_2015, cambios_2016, cambios_2017 = _cargar_datos(select_rep)

            if not df_duracion.empty and not df_distribucion.empty:
                fig = DuracionRepuestosPlotter(df_duracion, df_distribucion, filas).create_plot()

                aux5, col_2015, col_2016, col_2017, aux6 = st.columns((1, 1, 1, 1, 1))

                components.custom_metric(col_2015, "Sin cambios 2015", cambios_2015,
                                         CustomMetricColorsEnum.ROJO, CustomMetricColorsEnum.ROJO)

                components.custom_metric(col_2016, "Sin cambios 2016", cambios_2016,
                                         CustomMetricColorsEnum.AZUL, CustomMetricColorsEnum.AZUL)

                components.custom_metric(col_2017, "Sin cambios 2017", cambios_2017,
                                         CustomMetricColorsEnum.AMARILLO, CustomMetricColorsEnum.AMARILLO)

                st.plotly_chart(fig)

