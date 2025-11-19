import streamlit as st

from utils.streamlit_utils import centered_title, select_box_tipo_repuesto
from utils.exception_utils import execute_safely

from viewmodels.consumo.prevision.plotter import PrevisionPlotter

from config.constants import (MULTIPLE_PLOT_BOX_HEIGHT, PLOT_BOX_HEIGHT, DISTANCE_COLS_CENTER_TITLE,
                              DISTANCE_COLS_SELECTBIGGER_PLOT, PAG_PREVISION, SELECT_BOX_HEIGHT)

@execute_safely
def consumo_prevision():
    st.title(PAG_PREVISION)

    aux1, titulo_col, aux2 = st.columns(DISTANCE_COLS_CENTER_TITLE)
    config_col, graficos_col = st.columns(DISTANCE_COLS_SELECTBIGGER_PLOT)

    tipo_repuesto = select_box_tipo_repuesto(config_col, "FORECAST_REPUESTO")

    if tipo_repuesto:
        figs, titulo = PrevisionPlotter(tipo_repuesto).create_plot()

        if figs is None and titulo is None:
            with graficos_col.container(height=SELECT_BOX_HEIGHT):
                st.text("No hay datos de este repuesto.")
        else:
            centered_title(titulo_col, titulo)

            with graficos_col.container(height=MULTIPLE_PLOT_BOX_HEIGHT):
                for fig in figs:
                    with st.container(height=PLOT_BOX_HEIGHT):
                        st.plotly_chart(fig)


