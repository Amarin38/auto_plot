import streamlit as st

from config.constants_views import PAG_DURACION, DURACION_TAB_BOX_HEIGHT, HTML_SIN_CAMBIOS
from utils.common_utils import CommonUtils
from viewmodels.consumo.duracion_rep.plotter import DuracionRepuestosPlotter
from utils.exception_utils import execute_safely
from presentation.streamlit_components import SelectBoxComponents

@st.cache_data(ttl=200, show_spinner=False)
def _generar_grafico_duracion(select_rep):
    duracion = DuracionRepuestosPlotter(select_rep)

    return (duracion.create_plot(),
            duracion.calcular_sin_cambios("2015"),
            duracion.calcular_sin_cambios("2016"),
            duracion.calcular_sin_cambios("2017"))

@execute_safely
def duracion_repuestos():
    select = SelectBoxComponents()
    utils = CommonUtils()
    st.title(PAG_DURACION)

    # with st.container(height=DURACION_TAB_BOX_HEIGHT):
    aux1, aux2, rep_col, aux3, datos = st.columns((0.5, 0.5, 0.75, 0.3, 0.5))

    select_rep = select.select_box_repuesto(rep_col, "DURACION_REPUESTO_GENERAL")

    with st.container(height=DURACION_TAB_BOX_HEIGHT):
        if select_rep:
            with st.spinner("Cargando duraciones..."):
                duracion, cambios_2015, cambios_2016, cambios_2017 = utils.run_in_threads(
                    lambda: _generar_grafico_duracion(select_rep),
                    max_workers=6
                )

            st.plotly_chart(duracion)

            with datos.container(height=155):
                st.write(f"{HTML_SIN_CAMBIOS} Sin cambios en 2015: {cambios_2015}</p>",
                            unsafe_allow_html=True)
                st.write(f"{HTML_SIN_CAMBIOS} Sin cambios en 2016: {cambios_2016}</p>",
                            unsafe_allow_html=True)
                st.write(f"{HTML_SIN_CAMBIOS} Sin cambios en 2017: {cambios_2017}</p>",
                            unsafe_allow_html=True)

