import sys, os

import streamlit as st


if os.name == "nt":
    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
elif os.name == "posix":
    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../..")))

from src.utils.streamlit_utils import centered_title, select_box_tipo_repuesto
from src.utils.exception_utils import execute_safely

from src.plot.forecast_plotter import ForecastPlotter

from src.config.constants import (MULTIPLE_PLOT_BOX_HEIGHT, PLOT_BOX_HEIGHT, DISTANCE_COLS_CENTER_TITLE,
                                  DISTANCE_COLS_SELECTBIGGER_PLOT, PAG_PREVISION)

@execute_safely
def forecast_page():
    st.title(PAG_PREVISION)
    aux1, titulo_col, aux2 = st.columns(DISTANCE_COLS_CENTER_TITLE)
    config_col, graficos_col = st.columns(DISTANCE_COLS_SELECTBIGGER_PLOT)

    repuesto = select_box_tipo_repuesto(config_col, "FORECAST_REPUESTO")
    figs, titulo = ForecastPlotter(repuesto).create_plot()

    if repuesto:
        centered_title(titulo_col, titulo)

    with graficos_col.container(height=MULTIPLE_PLOT_BOX_HEIGHT):
        for fig in figs if figs is not None else figs:
            with st.container(height=PLOT_BOX_HEIGHT):
                st.plotly_chart(fig)
