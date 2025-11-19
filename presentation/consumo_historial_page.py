import streamlit as st

from config.constants import PAG_HISTORIAL, DISTANCE_COLS_SELECTBIGGER_PLOT, DISTANCE_COLS_CENTER_TITLE, \
    PLOT_BOX_HEIGHT, SELECT_BOX_HEIGHT
from utils.streamlit_utils import select_box_tipo_repuesto, centered_title
from viewmodels.consumo.historial.plotter import HistorialPlotter


def consumo_historial():
    st.title(PAG_HISTORIAL)

    aux1, titulo_col, aux2 = st.columns(DISTANCE_COLS_CENTER_TITLE)
    select_boxes, plot = st.columns(DISTANCE_COLS_SELECTBIGGER_PLOT)

    repuesto = select_box_tipo_repuesto(select_boxes, "HISTORIAL_REPUESTO")

    if repuesto:
        fig, titulo = HistorialPlotter(repuesto).create_plot()

        if fig and titulo:
            centered_title(titulo_col, titulo)
            with plot.container(height=PLOT_BOX_HEIGHT):
                st.plotly_chart(fig)
        else:
            with plot.container(height=SELECT_BOX_HEIGHT):
                st.text("No hay datos de este repuesto.")

