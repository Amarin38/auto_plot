import streamlit as st

from config.constants_common import COMPARACION_CABECERA_KEY, COMPARACION_TIPO_REP_KEY, COMPARACION_PERIODO_KEY
from config.constants_views import PAG_COMPARACION_CONSUMO, PLACEHOLDER, MULTI_SELECT_BOX_HEIGHT
from config.enums import CabecerasEnum
from presentation.streamlit_components import SelectBoxComponents
from viewmodels.consumo.comparacion.plotter import ConsumoComparacionPlotter
from viewmodels.consumo.comparacion.vm import ConsumoComparacionVM


@st.cache_data(ttl=200, show_spinner=False, show_time=True)
def _cargar_datos(cabecera, tipo_rep, periodo):
    return ConsumoComparacionVM().get_df_cabecera_and_tipo_rep_and_periodo(cabecera, tipo_rep, periodo)


def consumo_comparacion():
    select = SelectBoxComponents()
    st.title(PAG_COMPARACION_CONSUMO)

    izq, centro, der = st.columns([1.5,2.6,3])

    with izq.container(height=MULTI_SELECT_BOX_HEIGHT, vertical_alignment='center'):
            cabecera = st.selectbox(
                "Selecciona la cabecera:",
                CabecerasEnum,
                index=None,
                placeholder=PLACEHOLDER,
                key=COMPARACION_CABECERA_KEY
            )

    tipo_rep = select.multi_select_box_tipo_rep_comparacion(centro, COMPARACION_TIPO_REP_KEY)
    periodo = select.multi_select_box_periodo(der, COMPARACION_PERIODO_KEY)

    with (st.container(height=600)):
        if cabecera and tipo_rep and periodo:
            with st.spinner("Cargando comparaciones..."):
                df = _cargar_datos(cabecera, tipo_rep, periodo)

            if len(df):
                plot = ConsumoComparacionPlotter(df, cabecera, tipo_rep, periodo).create_plot()
                st.plotly_chart(plot)
            else:
                st.write("Selecciona un período o cabecera válidos.")
        else:
            st.write("Selecciona un cabecera, una tipo de repuesto y un período válido.")

