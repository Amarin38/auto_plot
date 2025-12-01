import streamlit as st

from config.constants_views import PAG_DURACION, DURACION_TAB_BOX_HEIGHT, HTML_SIN_CAMBIOS
from viewmodels.consumo.duracion_rep.plotter import DuracionRepuestosPlotter
from utils.exception_utils import execute_safely
from presentation.streamlit_components import SelectBoxComponents


@execute_safely
def duracion_repuestos():
    select = SelectBoxComponents()
    st.title(PAG_DURACION)

    with st.container(height=DURACION_TAB_BOX_HEIGHT):
        aux1, aux2, rep_col, aux3, datos = st.columns((0.5, 0.3, 1, 0.3, 0.5))

        select_rep = select.select_box_repuesto(rep_col, "DURACION_REPUESTO_GENERAL")

        if select_rep:
            duracion = DuracionRepuestosPlotter(select_rep)

            st.plotly_chart(duracion.create_plot())
            datos.write(f"{HTML_SIN_CAMBIOS} Sin cambios en 2015: {duracion.calcular_sin_cambios("2015")}</p>",
                        unsafe_allow_html=True)
            datos.write(f"{HTML_SIN_CAMBIOS} Sin cambios en 2016: {duracion.calcular_sin_cambios("2016")}</p>",
                        unsafe_allow_html=True)
            datos.write(f"{HTML_SIN_CAMBIOS} Sin cambios en 2017: {duracion.calcular_sin_cambios("2017")}</p>",
                        unsafe_allow_html=True)
