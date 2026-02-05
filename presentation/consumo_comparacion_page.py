import streamlit as st

from config.constants_views import PAG_COMPARACION_CONSUMO
from domain.entities.consumo_comparacion import ConsumoComparacion
from presentation.streamlit_components import SelectBoxComponents
from viewmodels.consumo.comparacion.plotter import ConsumoComparacionPlotter


def consumo_comparacion():
    select = SelectBoxComponents()
    st.title(PAG_COMPARACION_CONSUMO)

    a, b, c = st.columns([1.5,3,3])

    # TODO: aplicar cacheo
    # TODO: aplicar multithreading

    cabecera = select.select_box_cabecera(a, "CABECERA_COMPARACION")
    tipo_rep = select.multi_select_box_tipo_rep_comparacion(b, "REP_COMPARACION")
    periodo = select.multi_select_box_periodo(c, "PERIODO")

    with st.container(height=600):
        if cabecera and tipo_rep and periodo:
            table, plot = ConsumoComparacionPlotter(cabecera, tipo_rep, periodo).create_plot()
            st.write(table)
            st.write(plot)

            # st.plotly_chart()
        st.write("Selecciona una cabecera, una tipo de repuesto y un período válido.")