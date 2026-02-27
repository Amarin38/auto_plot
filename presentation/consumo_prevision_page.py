import streamlit as st

from presentation.streamlit_components import SelectBoxComponents, OtherComponents
from utils.exception_utils import execute_safely
from viewmodels.consumo.prevision.data_vm import PrevisionDataVM

from viewmodels.consumo.prevision.plotter import PrevisionPlotter

from config.constants_views import (PLOT_BOX_HEIGHT, DISTANCE_COLS_CENTER_TITLE, DISTANCE_COLS_SELECTBIGGER_PLOT,
                                     PAG_PREVISION)
from viewmodels.consumo.prevision.vm import PrevisionVM


@st.cache_data(ttl=200, show_spinner=False, show_time=True)
def _cargar_datos(tipo_repuesto):
    return PrevisionDataVM().get_df_by_tipo_repuesto(tipo_repuesto), PrevisionVM().get_df_by_tipo_repuesto(tipo_repuesto)


@execute_safely
def consumo_prevision():
    select = SelectBoxComponents()
    other = OtherComponents()

    st.title(PAG_PREVISION)

    aux1, titulo_col, aux2 = st.columns(DISTANCE_COLS_CENTER_TITLE)
    config_col, graficos_col = st.columns(DISTANCE_COLS_SELECTBIGGER_PLOT)

    tipo_repuesto = select.select_box_tipo_repuesto(config_col, "FORECAST_REPUESTO")

    if tipo_repuesto:
        with config_col:
            with st.spinner("Cargando previsiones..."):
                df_data, df_forecast = _cargar_datos(tipo_repuesto)

            if not df_data.empty and not df_forecast.empty:
                figs, titulo = PrevisionPlotter(df_data, df_forecast, tipo_repuesto).create_plot()
                other.centered_title(titulo_col, titulo)

                with graficos_col:
                    for fig in figs:
                        with st.container(height=PLOT_BOX_HEIGHT):
                            st.plotly_chart(fig)
            else:
                other.mensaje_falta_rep(graficos_col)


