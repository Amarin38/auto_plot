import time

import streamlit as st

from config.constants_views import PAG_CONSUMO_OBLIGATORIO
from presentation.streamlit_components import SelectBoxComponents
from utils.common_utils import CommonUtils
from viewmodels.consumo.obligatorio.plotter import ConsumoObligatorioPlotter

@st.cache_data(ttl=200, show_spinner="Cargando consumo obligatorio...", show_time=True)
def _generar_grafico_obligatorio(repuesto):
    return ConsumoObligatorioPlotter(repuesto).create()

def consumo_obligatorio():
    select = SelectBoxComponents()
    utils = CommonUtils()
    st.title(PAG_CONSUMO_OBLIGATORIO)

    sel, plot = st.columns([0.45, 1])

    repuesto = select.select_box_consumo_obligatorio(sel, "SELECT_BOX_CONSUMO_OBLIGATORIO")

    if repuesto:
        fig = utils.run_in_threads(lambda: _generar_grafico_obligatorio(repuesto), max_workers=4)
        st.container(height=555).plotly_chart(fig)
