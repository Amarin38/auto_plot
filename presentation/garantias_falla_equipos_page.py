import streamlit as st

from utils.exception_utils import execute_safely
from utils.streamlit_utils import select_box_tipo_repuesto, select_box_cabecera

from config.constants import FALLA_TAB_BOX_HEIGHT, PAG_FALLA_GARANTIAS, TABS_FALLAS

from viewmodels.garantias.falla.plotter import FallaGarantiasPlotter
from viewmodels.garantias.consumo.plotter import ConsumoGarantiasPlotter


@execute_safely
def garantias_falla_equipos():
    st.title(PAG_FALLA_GARANTIAS)
    with st.container(height=FALLA_TAB_BOX_HEIGHT):
        aux1, cabecera_col, repuesto_col, aux2 = st.columns((1, 1, 1, 1))

        cabecera = select_box_cabecera(cabecera_col, "FALLA_GAR_CABECERA")
        tipo_repuesto = select_box_tipo_repuesto(repuesto_col, "FALLA_GAR_TIPO_REP")

        pie, bar = st.tabs(TABS_FALLAS)

        if cabecera and tipo_repuesto:
            with pie:
                pie_plot = FallaGarantiasPlotter(tipo_repuesto, cabecera).create_plot()
                if pie_plot is None:
                    pie.write("No existe información de la cabecera o el repuesto.")
                else:
                    st.plotly_chart(pie_plot)

            with bar:
                bar_plot = ConsumoGarantiasPlotter(tipo_repuesto, cabecera).create_plot()
                if bar_plot is None:
                    bar.write("No existe información de la cabecera o el repuesto.")
                else:
                    st.plotly_chart(bar_plot)