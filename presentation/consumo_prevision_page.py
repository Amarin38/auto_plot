import time

import streamlit as st

from presentation.streamlit_components import SelectBoxComponents, OtherComponents
from utils.common_utils import CommonUtils
from utils.exception_utils import execute_safely

from viewmodels.consumo.prevision.plotter import PrevisionPlotter

from config.constants_views import (PLOT_BOX_HEIGHT, DISTANCE_COLS_CENTER_TITLE, DISTANCE_COLS_SELECTBIGGER_PLOT,
                                     PAG_PREVISION)

@st.cache_data(ttl=200, show_spinner=False, show_time=True)
def _generar_grafico_prevision(tipo_repuesto):
    return PrevisionPlotter(tipo_repuesto).create_plot()

@execute_safely
def consumo_prevision():
    select = SelectBoxComponents()
    other = OtherComponents()
    utils = CommonUtils()

    st.title(PAG_PREVISION)

    aux1, titulo_col, aux2 = st.columns(DISTANCE_COLS_CENTER_TITLE)
    config_col, graficos_col = st.columns(DISTANCE_COLS_SELECTBIGGER_PLOT)

    tipo_repuesto = select.select_box_tipo_repuesto(config_col, "FORECAST_REPUESTO")

    if tipo_repuesto:
        with config_col:
            with st.spinner("Cargando previsiones..."):
                figs, titulo = utils.run_in_threads(lambda: _generar_grafico_prevision(tipo_repuesto), max_workers=4)

        if figs and titulo:
            other.centered_title(titulo_col, titulo)

            with graficos_col:
                for fig in figs:
                    with st.container(height=PLOT_BOX_HEIGHT):
                        st.plotly_chart(fig)
        else:
            other.mensaje_falta_rep(graficos_col)


