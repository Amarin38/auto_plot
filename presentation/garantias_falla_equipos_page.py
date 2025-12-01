import streamlit as st

from utils.exception_utils import execute_safely
from presentation.streamlit_components import SelectBoxComponents

from config.constants_views import FALLA_TAB_BOX_HEIGHT, PAG_FALLA_GARANTIAS, FALLA_GARANTIAS_BOX_HEIGHT

from viewmodels.garantias.falla.plotter import FallaGarantiasPlotter
from viewmodels.garantias.consumo.plotter import ConsumoGarantiasPlotter


@execute_safely
def garantias_falla_equipos():
    select = SelectBoxComponents()
    st.title(PAG_FALLA_GARANTIAS)

    with st.container(height=FALLA_TAB_BOX_HEIGHT):
        aux1, cabecera_col, repuesto_col, aux2 = st.columns((1, 1, 1, 1))

        cabecera = select.select_box_cabecera(cabecera_col, "FALLA_GAR_CABECERA")
        tipo_repuesto = select.select_box_tipo_repuesto(repuesto_col, "FALLA_GAR_TIPO_REP")


        if cabecera and tipo_repuesto:
            pie_col, bar_col = st.columns((1,1.5))

            pie_plot = FallaGarantiasPlotter(tipo_repuesto, cabecera).create_plot()
            bar_plot = ConsumoGarantiasPlotter(tipo_repuesto, cabecera).create_plot()

            if pie_plot is None or bar_plot is None:
                st.write("No existe información de la cabecera o el repuesto.")
            else:
                with pie_col.container(height=FALLA_GARANTIAS_BOX_HEIGHT):
                    st.plotly_chart(pie_plot)
                with bar_col.container(height=FALLA_GARANTIAS_BOX_HEIGHT):
                    st.plotly_chart(bar_plot)