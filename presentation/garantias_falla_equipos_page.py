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


        pie_col, bar_col = st.columns((1,1.5))

        with pie_col.container(height=FALLA_GARANTIAS_BOX_HEIGHT):
            pie_plot = FallaGarantiasPlotter(tipo_repuesto, cabecera).create_plot()

            if pie_plot:
                st.plotly_chart(pie_plot)
            else:
                st.write("Selecciona un repuesto o cabecera válidos para mostrar los fallos.")

        with bar_col.container(height=FALLA_GARANTIAS_BOX_HEIGHT):
            bar_plot = ConsumoGarantiasPlotter(tipo_repuesto, cabecera).create_plot()

            if bar_plot:
                st.plotly_chart(bar_plot)
            else:
                st.write("Selecciona un repuesto o cabecera válidos para mostrar los consumos de garantías y trasnferencias.")