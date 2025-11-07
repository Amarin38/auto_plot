import streamlit as st

from utils.exception_utils import execute_safely
from utils.streamlit_utils import select_box_tipo_repuesto, select_box_cabecera

from config.constants import FALLA_TAB_BOX_HEIGHT, PAG_FALLA_GARANTIAS, TABS_FALLAS

from viewmodels.plot.falla_garantias_plotter import FallasGarantiasPlotter
from viewmodels.plot.consumo_garantias_plotter import ConsumoGarantiasPlotter


@execute_safely
def falla_equipos_garantias():
    st.title(PAG_FALLA_GARANTIAS)
    with st.container(height=FALLA_TAB_BOX_HEIGHT):
        aux1, cabecera_col, repuesto_col, aux2 = st.columns((1, 1, 1, 1))

        cabecera = select_box_cabecera(cabecera_col, "FALLA_GAR_CABECERA")
        tipo_repuesto = select_box_tipo_repuesto(repuesto_col, "FALLA_GAR_TIPO_REP")

        pie, bar = st.tabs(TABS_FALLAS)

        with pie:
            pie_plot = FallasGarantiasPlotter(cabecera, tipo_repuesto).create_plot()
            st.plotly_chart(pie_plot)

        with bar:
            consumo_plot = ConsumoGarantiasPlotter(cabecera, tipo_repuesto).create_plot()
            st.plotly_chart(consumo_plot)