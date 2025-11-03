import sys, os

import streamlit as st

if os.name == "nt":
    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
elif os.name == "posix":
    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../..")))

from utils.exception_utils import execute_safely
from utils.streamlit_utils import select_box_tipo_repuesto, select_box_cabecera

from config.constants import FALLA_TAB_BOX_HEIGHT, PAG_FALLA_GARANTIAS, TABS_FALLAS

from plot.falla_garantias_plotter import FallasGarantiasPlotter
from plot.consumo_garantias_plotter import ConsumoGarantiasPlotter


@execute_safely
def falla_equipos_garantias_page():
    st.title(PAG_FALLA_GARANTIAS)
    with st.container(height=FALLA_TAB_BOX_HEIGHT):
        pie, bar = st.tabs(TABS_FALLAS)

        # TODO: cambiar para que tome de los mismos 2 select_boxes para hacer ambos gráficos a la vez y
        #   cambiarlo con tabs
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