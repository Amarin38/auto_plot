import streamlit as st

from config.constants_views import PAG_HISTORIAL, DISTANCE_COLS_SELECTBIGGER_PLOT, DISTANCE_COLS_CENTER_TITLE, \
    PLOT_BOX_HEIGHT, SELECT_BOX_HEIGHT
from viewmodels.consumo.historial.plotter import HistorialPlotter
from presentation.streamlit_components import SelectBoxComponents, OtherComponents


def consumo_historial():
    select = SelectBoxComponents()
    other = OtherComponents()

    st.title(PAG_HISTORIAL)

    aux1, titulo_col, aux2 = st.columns(DISTANCE_COLS_CENTER_TITLE)
    select_boxes, plot = st.columns(DISTANCE_COLS_SELECTBIGGER_PLOT)

    repuesto = select.select_box_tipo_repuesto(select_boxes, "HISTORIAL_REPUESTO")

    if repuesto:
        fig, titulo = HistorialPlotter(repuesto).create_plot()

        if fig and titulo:
            other.centered_title(titulo_col, titulo)

            with plot.container(height=PLOT_BOX_HEIGHT):
                st.plotly_chart(fig)
        else:
            other.mensaje_falta_rep(plot)
