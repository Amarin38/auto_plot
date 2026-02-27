import streamlit as st

from config.constants_views import PAG_HISTORIAL, DISTANCE_COLS_SELECTBIGGER_PLOT, DISTANCE_COLS_CENTER_TITLE, \
    PLOT_BOX_HEIGHT, SELECT_BOX_HEIGHT
from config.enums import RepuestoEnum, TendenciaEnum
from viewmodels.consumo.historial.plotter import HistorialPlotter
from presentation.streamlit_components import SelectBoxComponents, OtherComponents
from viewmodels.consumo.historial.vm import HistorialConsumoVM


@st.cache_data(ttl=200, show_spinner=False, show_time=True)
def _cargar_datos(repuesto: RepuestoEnum):
    return HistorialConsumoVM().get_df_tipo_repuesto(repuesto)


def consumo_historial():
    select = SelectBoxComponents()
    other = OtherComponents()

    st.title(PAG_HISTORIAL)

    aux1, titulo_col, aux2 = st.columns(DISTANCE_COLS_CENTER_TITLE)
    select_boxes, plot = st.columns(DISTANCE_COLS_SELECTBIGGER_PLOT)

    repuesto = select.select_box_tipo_repuesto(select_boxes, "HISTORIAL_REPUESTO")

    with select_boxes.container(height=SELECT_BOX_HEIGHT):
        tendencia = st.selectbox("Selecciona la tendencia:", TendenciaEnum)

    if repuesto:
        with st.spinner("Cargando historial de consumo..."):
            df = _cargar_datos(repuesto)

        if not df.empty:
            fig, titulo = HistorialPlotter(df, repuesto, tendencia).create_plot()

            other.centered_title(titulo_col, titulo)

            with plot.container(height=PLOT_BOX_HEIGHT):
                st.plotly_chart(fig)
        else:
            other.mensaje_falta_rep(plot)
