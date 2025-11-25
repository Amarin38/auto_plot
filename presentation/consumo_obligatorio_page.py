
import streamlit as st

from config.constants import PAG_CONSUMO_OBLIGATORIO
from presentation.streamlit_components import SelectBoxComponents
from viewmodels.consumo.obligatorio.plotter import ConsumoObligatorioPlotter

def consumo_obligatorio():
    select = SelectBoxComponents()
    st.title(PAG_CONSUMO_OBLIGATORIO)

    sel, plot = st.columns([0.45, 1])

    repuesto = select.select_box_consumo_obligatorio(sel, "SELECT_BOX_CONSUMO_OBLIGATORIO")

    if repuesto:
        st.container(height=555).plotly_chart(ConsumoObligatorioPlotter(repuesto).create())
