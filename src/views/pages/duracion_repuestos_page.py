import streamlit as st

from src.config.constants import PAG_DURACION, FALLA_TAB_BOX_HEIGHT
from src.config.enums import TipoDuracionEnum, RepuestoReparadoEnum
from src.plot.duracion_repuestos_plotter import DuracionRepuestosPlotter
from src.utils.exception_utils import execute_safely
from src.utils.streamlit_utils import select_box


@execute_safely
def duracion_repuestos_page():
    st.title(PAG_DURACION)

    with st.container(height=FALLA_TAB_BOX_HEIGHT):
        aux1, rep_col, tipo_rep_col, aux2 = st.columns((1, 1, 1, 1))

        with rep_col:
            select_rep = select_box(rep_col, "Selecciona el repuesto para ver su duracion:", RepuestoReparadoEnum)

        with tipo_rep_col:
            select_tipo = select_box(tipo_rep_col, "Selecciona el tipo de duracion:", TipoDuracionEnum)


        if select_tipo is not None and select_rep is not None:
            st.plotly_chart(DuracionRepuestosPlotter(select_rep, select_tipo).create_plot())

