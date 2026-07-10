from typing import Any, Dict

import pandas as pd
import streamlit as st

from utils.exception_utils import execute_safely
from presentation.streamlit_components import SelectBoxComponents

from config.constants_views import FALLA_TAB_BOX_HEIGHT, PAG_FALLA_GARANTIAS, FALLA_GARANTIAS_BOX_HEIGHT

from plotters.garantias_fallas_plotter import FallaGarantiasPlotter
from viewmodels.garantias_vm import ConsumoGarantiasVM, FallaGarantiasVM, DatosGarantiasVM



@st.cache_data(ttl=200, show_spinner=False)
def _cargar_datos_pie(tipo_repuesto, cabecera) -> Dict[str, Any]:
    vm_datos = DatosGarantiasVM()

    return {
        "rep_cabecera": FallaGarantiasVM().get_df_by_tipo_and_cabecera(tipo_repuesto, cabecera),
        "min_d": vm_datos.get_min_date("FechaIngreso"),
        "max_d": vm_datos.get_max_date("FechaIngreso")
    }


@st.cache_data(ttl=200, show_spinner=False)
def _cargar_datos_bar(tipo_repuesto, cabecera) -> pd.DataFrame:
    return ConsumoGarantiasVM().get_df_by_tipo_and_cabecera(tipo_repuesto, cabecera)


@execute_safely
def garantias_falla_equipos() -> None:
    df_pie, df_bar = None, None
    select = SelectBoxComponents()
    st.title(PAG_FALLA_GARANTIAS)

    with st.container(height=FALLA_TAB_BOX_HEIGHT):
        _, cabecera_col, repuesto_col, _ = st.columns((1, 1, 1, 1))

        cabecera = select.select_box_cabecera(cabecera_col, "FALLA_GAR_CABECERA")
        tipo_repuesto = select.select_box_tipo_repuesto(repuesto_col, "FALLA_GAR_TIPO_REP")

        pie_col, bar_col = st.columns((1,1.5))

        if cabecera and tipo_repuesto:
            with st.spinner("Cargando datos..."):
                datos_pie = _cargar_datos_pie(tipo_repuesto, cabecera)
                df_bar = _cargar_datos_bar(tipo_repuesto, cabecera)

                df_pie = datos_pie["rep_cabecera"]
                min_date = datos_pie["min_d"]
                max_date = datos_pie["max_d"]

            plotter = FallaGarantiasPlotter(min_date, max_date)

            with pie_col.container(height=FALLA_GARANTIAS_BOX_HEIGHT):
                if len(df_pie) and min_date and max_date:
                    st.plotly_chart(
                        plotter.create_falla_plot(df_pie)
                    )
                else:
                    st.write("Selecciona un repuesto o cabecera válidos para mostrar los fallos.")

            with bar_col.container(height=FALLA_GARANTIAS_BOX_HEIGHT):
                if len(df_bar):
                    st.plotly_chart(
                        plotter.create_consumo_plot(df_bar)
                    )
                else:
                    st.write("Selecciona un repuesto o cabecera válidos para mostrar los consumos de garantías y trasnferencias.")

