import streamlit as st

from presentation.streamlit_components import SelectBoxComponents, OtherComponents, ButtonComponents
from utils.exception_utils import execute_safely

from viewmodels.consumo.indice.plotter import  IndexPlotter

from config.constants_colors import COLORS
from config.constants_views import (PLOT_BOX_HEIGHT, DISTANCE_COLS_CENTER_TITLE, DISTANCE_COLS_SELECTBIGGER_PLOT,
                                    PAG_INDICES, SELECT_BOX_HEIGHT, FULL_PLOT_BOX_HEIGHT, DESVIACION_BOX_HEIGHT)

from viewmodels.consumo.indice.desviacion.plotter import DeviationPlotter
from viewmodels.processing.compute.compute_desviacion_indices import DeviationTrend


@execute_safely
def consumo_indice() -> None:
    select = SelectBoxComponents()
    other = OtherComponents()
    button = ButtonComponents()

    st.title(PAG_INDICES)

    other.bar_tabs("#B2B9B0", "#BAC1B8", "#828E82",
             "#0C7C59", "#4D9078", "#0C7C59")

    indice, desviacion = st.tabs(["📊 Indices", "📊↕️ Desviaciones de indices"])


    with indice:
        aux1, titulo_col, aux2 = st.columns(DISTANCE_COLS_CENTER_TITLE)
        config_col, graficos_col = st.columns(DISTANCE_COLS_SELECTBIGGER_PLOT)

        repuesto = select.select_box_tipo_repuesto(config_col, "INDEX_REPUESTO")
        tipo_indice = select.select_box_tipo_indice(config_col, "INDEX_TIPO_INDICE")

        if repuesto and tipo_indice:
            figs, titulo = IndexPlotter(tipo_indice, repuesto).create_plot()

            if figs and titulo:
                other.centered_title(titulo_col, titulo)

                with graficos_col:
                    for fig in figs if figs is not None else figs:
                        with st.container(height=PLOT_BOX_HEIGHT):
                            st.plotly_chart(fig)

            else:
                with graficos_col.container(height=SELECT_BOX_HEIGHT):
                    st.text("No hay datos de este repuesto.")


    with desviacion.container(height=DESVIACION_BOX_HEIGHT):
        aux, recargar, selectbox = st.columns([5.65,0.3, 2])

        if recargar.button(label="🔃", type="secondary", use_container_width=True):
            DeviationTrend().calculate()

        repuesto = select.select_box_tipo_repuesto(selectbox, "DESVIACION_TIPO_REP")

        grafico, explicacion = st.columns([3, 1])

        with grafico.container(height=FULL_PLOT_BOX_HEIGHT):
            if repuesto:
                st.plotly_chart(DeviationPlotter(repuesto).create_plot())
            else:
                st.plotly_chart(DeviationPlotter(None).create_plot())

        with explicacion.container(height=FULL_PLOT_BOX_HEIGHT):
            menor = f"<font color={COLORS[9]}>**menor**</font>"
            mayor = f"<font color={COLORS[2]}>**mayor**</font>"
            cabecera = f"<font color={COLORS[0]}>**cabecera**</font>"

            st.write(f"""
                Este gráfico muestra, en %, cuánto se desvió cada 
                {cabecera} respecto de la media de todos los índices de consumo registrados hasta la fecha.

                Cálculo para la desviación porcentual:
                """, unsafe_allow_html=True)
            st.latex(r'\frac{media - media\ de\ medias}{media\ de\ medias}')

            st.text("\n")

            st.write(f"""
                **Valores positivos** (➕)\n 
                - Cuanto {mayor} el porcentaje, {mayor} la cantidad de veces que la {cabecera} en cuestión
                  superó la media en cada índice de consumo. \n
                **Valores negativos** (➖)\n 
                - Cuanto {menor} el porcentaje, {menor} la cantidad de veces que la {cabecera} en cuestión
                  superó la media en cada índice de consumo.\n
                """, unsafe_allow_html=True)
