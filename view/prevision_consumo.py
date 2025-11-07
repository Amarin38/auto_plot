import streamlit as st

from utils.streamlit_utils import centered_title, select_box_tipo_repuesto
from utils.exception_utils import execute_safely

from viewmodels.plot.prevision_plotter import ForecastPlotter

from config.constants import (MULTIPLE_PLOT_BOX_HEIGHT, PLOT_BOX_HEIGHT, DISTANCE_COLS_CENTER_TITLE,
                              DISTANCE_COLS_SELECTBIGGER_PLOT, PAG_PREVISION)

@execute_safely
def prevision():
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
