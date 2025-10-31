import sys, os

import streamlit as st

from src.config.constants import FULL_PLOT_BOX_HEIGHT, TAB_BOX_HEIGHT, PAG_DESVIACIONES, COLORS, T_ORANGE
from src.db_data.crud_services import ServiceRead
from src.db_data.models.services_model.deviation_model import DeviationModel

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
from src.plot.deviation_plotter import DeviationPlotter
from src.utils.exception_utils import execute_safely

@st.fragment
@execute_safely
def deviation_page():
    st.title(PAG_DESVIACIONES)
    with st.container(height=TAB_BOX_HEIGHT):
        plot, data = st.tabs([" 📊 Gráfico", " ℹ️ Datos"])

        with plot:
            grafico, explicacion = st.columns([3,1])

            with grafico.container(height=FULL_PLOT_BOX_HEIGHT):
                st.plotly_chart(DeviationPlotter().create_plot())
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
        with data:
            st.dataframe(ServiceRead.all_df(DeviationModel), height=FULL_PLOT_BOX_HEIGHT)
