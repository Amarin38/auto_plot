import sys, os
import streamlit as st

from src.utils.streamlit_utils import centered_title, select_box

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
from src.plot.index_plotter import  IndexPlotter

from src.utils.exception_utils import execute_safely

from src.config.constants import (MULTIPLE_PLOT_BOX_HEIGHT, PLOT_BOX_HEIGHT, DISTANCE_COLS_CENTER_TITLE,
                                  DISTANCE_COLS_SELECTBIGGER_PLOT)
from src.config.enums import IndexTypeEnum, RepuestoEnum


@execute_safely
def index_page() -> None:
    aux1, titulo_col, aux2 = st.columns(DISTANCE_COLS_CENTER_TITLE)
    config_col, graficos_col = st.columns(DISTANCE_COLS_SELECTBIGGER_PLOT)

    repuesto = select_box(config_col, "Selecciona el repuesto: ", RepuestoEnum)
    tipo_indice = select_box(config_col, "Selecciona el tipo de indice: ", IndexTypeEnum)

    figs, titulo = IndexPlotter(tipo_indice, repuesto).create_plot()

    if repuesto and tipo_indice:
        centered_title(titulo_col, titulo)

    with graficos_col.container(height=MULTIPLE_PLOT_BOX_HEIGHT):
        for fig in figs if figs is not None else figs:
            with st.container(height=PLOT_BOX_HEIGHT):
                st.plotly_chart(fig)

