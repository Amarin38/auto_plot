import streamlit as st

from config.constants_views import PAG_COMPARACION_CONSUMO
from presentation.streamlit_components import SelectBoxComponents
from utils.common_utils import CommonUtils
from viewmodels.consumo.comparacion.plotter import ConsumoComparacionPlotter

@st.cache_data(ttl=200, show_spinner=False, show_time=True)
def _generar_grafico_comparacion(cabecera, tipo_rep, periodo):
    return ConsumoComparacionPlotter(cabecera, tipo_rep, periodo).create_plot()

def consumo_comparacion():
    select = SelectBoxComponents()
    utils = CommonUtils()
    st.title(PAG_COMPARACION_CONSUMO)

    a, b, c = st.columns([1.5,2.6,3])

    cabecera = select.select_box_cabecera(a, "CABECERA_COMPARACION")
    tipo_rep = select.multi_select_box_tipo_rep_comparacion(b, "REP_COMPARACION")
    periodo = select.multi_select_box_periodo(c, "PERIODO")

    with st.container(height=600):
        if cabecera and tipo_rep and periodo:
            with st.spinner("Cargando comparaciones..."):
                plot = utils.run_in_threads(lambda: _generar_grafico_comparacion(cabecera, tipo_rep, periodo), max_workers=2)

            st.plotly_chart(plot) if plot else st.write("Selecciona un período o cabecera válidos.")
        else:
            st.write("Selecciona un cabecera, una tipo de repuesto y un período válido.")

