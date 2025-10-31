import streamlit as st

from src.config.constants import PAG_DURACION, TABS_DURACION, DURACION_TAB_BOX_HEIGHT, HTML_SIN_CAMBIOS
from src.plot.duracion_repuestos_plotter import DuracionRepuestosPlotter
from src.utils.exception_utils import execute_safely
from src.utils.streamlit_utils import select_box_cabecera, select_box_repuesto, select_box_tipo_duracion


@execute_safely
def duracion_repuestos_page():
    st.title(PAG_DURACION)

    with st.container(height=DURACION_TAB_BOX_HEIGHT):
        general, por_cabecera = st.tabs(TABS_DURACION)

        with general:
            aux1, rep_col, tipo_rep_col, datos = st.columns((1, 1, 1, 1))

            select_rep = select_box_repuesto(rep_col, "DURACION_REPUESTO_GENERAL")
            select_tipo = select_box_tipo_duracion(tipo_rep_col, "DURACION_TIPO_DURACION_GENERAL")

            if select_tipo and select_rep:
                duracion = DuracionRepuestosPlotter(select_rep, select_tipo)

                st.plotly_chart(duracion.create_plot())
                datos.write(f"{HTML_SIN_CAMBIOS} Sin cambios en 2015: {duracion.calcular_sin_cambios("2015")}</p>",
                            unsafe_allow_html=True)
                datos.write(f"{HTML_SIN_CAMBIOS} Sin cambios en 2016: {duracion.calcular_sin_cambios("2016")}</p>",
                            unsafe_allow_html=True)
                datos.write(f"{HTML_SIN_CAMBIOS} Sin cambios en 2017: {duracion.calcular_sin_cambios("2017")}</p>",
                            unsafe_allow_html=True)


        with por_cabecera:
            aux1, cabecera_col, rep_col, tipo_rep_col, aux2 = st.columns((1, 1, 1, 1, 1))

            select_cabecera = select_box_cabecera(cabecera_col, "DURACION_CABECERA_TIPO")
            select_rep = select_box_repuesto(rep_col, "DURACION_REPUESTO_TIPO")
            select_tipo = select_box_tipo_duracion(tipo_rep_col, "DURACION_TIPO_DURACION_TIPO")

            if select_cabecera and select_rep and select_tipo:
                st.plotly_chart(DuracionRepuestosPlotter(select_rep, select_tipo, select_cabecera).create_plot())