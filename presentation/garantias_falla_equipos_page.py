from typing import Tuple

import pandas as pd
import streamlit as st
from pandas import DataFrame

from utils.exception_utils import execute_safely
from presentation.streamlit_components import SelectBoxComponents

from config.constants_views import FALLA_TAB_BOX_HEIGHT, PAG_FALLA_GARANTIAS, FALLA_GARANTIAS_BOX_HEIGHT
from viewmodels.garantias.consumo.vm import ConsumoGarantiasVM
from viewmodels.garantias.falla.datos_vm import DatosGarantiasVM

from viewmodels.garantias.falla.plotter import FallaGarantiasPlotter
from viewmodels.garantias.consumo.plotter import ConsumoGarantiasPlotter
from viewmodels.garantias.falla.vm import FallaGarantiasVM


@st.cache_data(ttl=200, show_spinner=False)
def _cargar_datos_pie(tipo_repuesto, cabecera) -> Tuple[DataFrame, str, str]:
    return (FallaGarantiasVM().get_df_by_tipo_rep_and_cabecera(tipo_repuesto, cabecera),
            DatosGarantiasVM().get_min_date(),
            DatosGarantiasVM().get_max_date())


@st.cache_data(ttl=200, show_spinner=False)
def _cargar_datos_bar(tipo_repuesto, cabecera) -> pd.DataFrame:
    return ConsumoGarantiasVM().get_df_by_tipo_rep_and_cabecera(tipo_repuesto, cabecera)


@execute_safely
def garantias_falla_equipos():
    df_pie, df_bar = None, None
    select = SelectBoxComponents()
    st.title(PAG_FALLA_GARANTIAS)

    with st.container(height=FALLA_TAB_BOX_HEIGHT):
        aux1, cabecera_col, repuesto_col, aux2 = st.columns((1, 1, 1, 1))

        cabecera = select.select_box_cabecera(cabecera_col, "FALLA_GAR_CABECERA")
        tipo_repuesto = select.select_box_tipo_repuesto(repuesto_col, "FALLA_GAR_TIPO_REP")

        pie_col, bar_col = st.columns((1,1.5))


        with aux1:
            if cabecera and tipo_repuesto:
                with st.spinner("Cargando datos..."):
                    df_pie, min_date, max_date = _cargar_datos_pie(tipo_repuesto, cabecera)
                    df_bar = _cargar_datos_bar(tipo_repuesto, cabecera)

                with pie_col.container(height=FALLA_GARANTIAS_BOX_HEIGHT):
                    if not df_pie.empty and min_date and max_date:
                        pie_plot = FallaGarantiasPlotter(df_pie, min_date, max_date).create_plot()

                        st.plotly_chart(pie_plot)
                    else:
                        st.write("Selecciona un repuesto o cabecera válidos para mostrar los fallos.")

                with bar_col.container(height=FALLA_GARANTIAS_BOX_HEIGHT):
                    if not df_bar.empty:
                        bar_plot = ConsumoGarantiasPlotter(df_bar).create_plot()

                        st.plotly_chart(bar_plot)
                    else:
                        st.write("Selecciona un repuesto o cabecera válidos para mostrar los consumos de garantías y trasnferencias.")

