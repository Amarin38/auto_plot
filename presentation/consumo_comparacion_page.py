import streamlit as st

from config.constants_views import PAG_COMPARACION_CONSUMO
from presentation.streamlit_components import SelectBoxComponents
from viewmodels.consumo.comparacion.plotter import ConsumoComparacionPlotter
from viewmodels.consumo.comparacion.vm import ConsumoComparacionVM


@st.cache_data(ttl=200, show_spinner=False, show_time=True)
def _cargar_datos(cabecera, tipo_rep, periodo):
    return ConsumoComparacionVM().get_df_cabecera_and_tipo_rep_and_periodo(cabecera, tipo_rep, periodo)


def consumo_comparacion():
    select = SelectBoxComponents()
    st.title(PAG_COMPARACION_CONSUMO)

    a, b, c = st.columns([1.5,2.6,3])

    cabecera = select.select_box_cabecera(a, "CABECERA_COMPARACION")
    tipo_rep = select.multi_select_box_tipo_rep_comparacion(b, "REP_COMPARACION")
    periodo = select.multi_select_box_periodo(c, "PERIODO")

    with (st.container(height=600)):
        if cabecera and tipo_rep and periodo:
            with st.spinner("Cargando comparaciones..."):
                df = _cargar_datos(cabecera, tipo_rep, periodo)

            if not df.empty:
                plot = ConsumoComparacionPlotter(df, cabecera, tipo_rep, periodo).create_plot()
                st.plotly_chart(plot)
            else:
                st.write("Selecciona un período o cabecera válidos.")
        else:
            st.write("Selecciona un cabecera, una tipo de repuesto y un período válido.")

