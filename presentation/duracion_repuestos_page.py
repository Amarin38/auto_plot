import streamlit as st

from config.constants_colors import RECUENTO_COLORS
from config.constants_views import PAG_DURACION, DURACION_TAB_BOX_HEIGHT, HTML_SIN_CAMBIOS, SELECT_BOX_HEIGHT
from utils.common_utils import CommonUtils
from viewmodels.consumo.duracion_rep.plotter import DuracionRepuestosPlotter
from utils.exception_utils import execute_safely
from presentation.streamlit_components import SelectBoxComponents, OtherComponents


@st.cache_data(ttl=200, show_spinner=False)
def _generar_grafico_duracion(select_rep, filas: int):
    duracion = DuracionRepuestosPlotter(select_rep, filas)

    return (duracion.create_plot(),
            duracion.calcular_sin_cambios("2015"),
            duracion.calcular_sin_cambios("2016"),
            duracion.calcular_sin_cambios("2017"))

@execute_safely
def duracion_repuestos():
    select = SelectBoxComponents()
    components = OtherComponents()
    utils = CommonUtils()
    colors = RECUENTO_COLORS

    st.title(PAG_DURACION)

    # with st.container(height=DURACION_TAB_BOX_HEIGHT):
    aux1, filas_col, rep_col, aux3 = st.columns((0.8, 0.5, 0.75, 0.8))

    select_rep = select.select_box_repuesto(rep_col, "DURACION_REPUESTO_GENERAL")

    with filas_col.container(height=SELECT_BOX_HEIGHT, vertical_alignment='center'):
        select_filas = st.selectbox("Seleccione la cantidad de cambios:", ["2 cambios", "4 cambios", "6 cambios"])

    if select_filas == "2 cambios": filas = 1
    elif select_filas == "4 cambios": filas = 2
    elif select_filas == "6 cambios": filas = 3

    with st.container(height=DURACION_TAB_BOX_HEIGHT):
        if select_rep:
            with st.spinner("Cargando duraciones..."):
                duracion, cambios_2015, cambios_2016, cambios_2017 = utils.run_in_threads(
                    lambda: _generar_grafico_duracion(select_rep, filas),
                    max_workers=6
                )

            aux5, col_2015, col_2016, col_2017, aux6 = st.columns((1, 1, 1, 1, 1))
            components.custom_metric(col_2015, "Sin cambios 2015", cambios_2015, colors[1], colors[1])
            components.custom_metric(col_2016, "Sin cambios 2016", cambios_2016, colors[2], colors[2])
            components.custom_metric(col_2017, "Sin cambios 2017", cambios_2017, colors[3], colors[3])

            st.plotly_chart(duracion)

