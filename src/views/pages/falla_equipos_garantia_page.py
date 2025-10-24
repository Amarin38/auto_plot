import sys, os

import streamlit as st


sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
from src.utils.exception_utils import execute_safely
from src.utils.streamlit_utils import select_box_tipo_repuesto, select_box_cabecera

from src.config.constants import FALLA_TAB_BOX_HEIGHT, PAG_FALLA_GARANTIAS, TABS_FALLAS

from src.plot.falla_garantias_plotter import FallasGarantiasPlotter
from src.plot.consumo_garantias_plotter import ConsumoGarantiasPlotter


@execute_safely
def falla_equipos_garantias_page():
    st.title(PAG_FALLA_GARANTIAS)
    with st.container(height=FALLA_TAB_BOX_HEIGHT):
        pie, bar = st.tabs(TABS_FALLAS)

        with pie:
            aux1, cabecera_col, repuesto_col, aux2 = st.columns((1, 1, 1, 1))

            cabecera = select_box_cabecera(cabecera_col, "FALLA_GAR_CABECERA_PIE")
            tipo_repuesto = select_box_tipo_repuesto(repuesto_col, "FALLA_GAR_TIPO_REP_PIE")

            pie_plot = FallasGarantiasPlotter(cabecera, tipo_repuesto).create_plot()
            st.plotly_chart(pie_plot)

        with bar:
            aux1, cabecera_col, repuesto_col, aux2 = st.columns((1, 1, 1, 1))

            cabecera = select_box_cabecera(cabecera_col, "FALLA_GAR_CABECERA_BAR")
            tipo_repuesto = select_box_tipo_repuesto(repuesto_col, "FALLA_GAR_TIPO_REP_BAR")

            consumo_plot = ConsumoGarantiasPlotter(cabecera, tipo_repuesto).create_plot()
            st.plotly_chart(consumo_plot)