
import streamlit as st

from config.constants import PAG_CONSUMO_OBLIGATORIO
from utils.streamlit_utils import select_box_consumo_obligatorio
from viewmodels.consumo.obligatorio.plotter import ConsumoObligatorioPlotter

def consumo_obligatorio():
    st.title(PAG_CONSUMO_OBLIGATORIO)

    select, plot = st.columns([0.45, 1])

    repuesto = select_box_consumo_obligatorio(select, "SELECT_BOX_CONSUMO_OBLIGATORIO")

    if repuesto:
        st.container(height=555).plotly_chart(ConsumoObligatorioPlotter(repuesto).create())
