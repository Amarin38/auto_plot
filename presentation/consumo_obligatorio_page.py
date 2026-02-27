import streamlit as st

from config.constants_views import PAG_CONSUMO_OBLIGATORIO
from presentation.streamlit_components import SelectBoxComponents
from utils.common_utils import CommonUtils
from viewmodels.consumo.obligatorio.plotter import ConsumoObligatorioPlotter
from viewmodels.consumo.obligatorio.vm import ConsumoObligatorioVM


@st.cache_data(ttl=200, show_time=True)
def _cargar_datos(repuesto):
    return ConsumoObligatorioVM().get_df_repuesto(repuesto)


def consumo_obligatorio():
    select = SelectBoxComponents()
    st.title(PAG_CONSUMO_OBLIGATORIO)

    sel, plot = st.columns([0.45, 1])

    repuesto = select.select_box_consumo_obligatorio(sel, "SELECT_BOX_CONSUMO_OBLIGATORIO")

    if repuesto:
        with st.spinner("Cargando consumo obligatorio..."):
            df = _cargar_datos(repuesto)

        if not df.empty:
            fig = ConsumoObligatorioPlotter(df).create()
            st.container(height=555).plotly_chart(fig)
