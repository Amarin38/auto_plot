import streamlit as st

from utils.streamlit_utils import centered_title, select_box_tipo_repuesto, select_box_tipo_indice
from utils.exception_utils import execute_safely

from viewmodels.plot.indice_consumo_plotter import  IndexPlotter

from config.constants import (MULTIPLE_PLOT_BOX_HEIGHT, PLOT_BOX_HEIGHT, DISTANCE_COLS_CENTER_TITLE,
                              DISTANCE_COLS_SELECTBIGGER_PLOT, PAG_INDICES)

@execute_safely
def indices_consumo() -> None:
    st.title(PAG_INDICES)
    aux1, titulo_col, aux2 = st.columns(DISTANCE_COLS_CENTER_TITLE)
    config_col, graficos_col = st.columns(DISTANCE_COLS_SELECTBIGGER_PLOT)

    repuesto = select_box_tipo_repuesto(config_col, "INDEX_REPUESTO")
    tipo_indice = select_box_tipo_indice(config_col, "INDEX_TIPO_INDICE")

    if repuesto and tipo_indice:
        figs, titulo = IndexPlotter(tipo_indice, repuesto).create_plot()
        centered_title(titulo_col, titulo)

        with graficos_col.container(height=MULTIPLE_PLOT_BOX_HEIGHT):
            for fig in figs if figs is not None else figs:
                with st.container(height=PLOT_BOX_HEIGHT):
                    st.plotly_chart(fig)

