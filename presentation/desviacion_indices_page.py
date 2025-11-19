import streamlit as st

from config.constants import FULL_PLOT_BOX_HEIGHT, TAB_BOX_HEIGHT, PAG_DESVIACION_INDICES, COLORS
from viewmodels.desviacion_indices.vm import DesviacionIndicesVM
from viewmodels.desviacion_indices.plotter import DeviationPlotter
from utils.exception_utils import execute_safely


@st.fragment
@execute_safely
def desviacion_indices():
    st.title(PAG_DESVIACION_INDICES)

    with st.container(height=TAB_BOX_HEIGHT):
        st.markdown("""
        <style>
        /* Tabs container */
        .stTabs [data-baseweb="tab-list"] {
            background-color: #B2B9B0;
            border-radius: 10px;
            padding: 4px 8px;
        }

        /* Normal tab */
        .stTabs [data-baseweb="tab"] {
            color: #BAC1B8;
            background-color: #828E82;
            border-radius: 10px;
            margin-right: 2px;
            padding: 6px 8px;
        }

        /* Hover */
        .stTabs [data-baseweb="tab"]:hover_unified {
            background-color: #0C7C59;
        }

        /* Active tab */
        .stTabs [aria-selected="true"] {
            background-color: #4D9078 !important;
            color: white !important;
        }
        
        /* Highlight */
        .stTabs [data-baseweb="tab-highlight"] {
            background-color: #0C7C59 !important;
        }
        </style>
        """, unsafe_allow_html=True)

        plot, data = st.tabs(["📊 Gráfico", "ℹ️ Datos"])

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
            st.dataframe(DesviacionIndicesVM().get_df(), height=FULL_PLOT_BOX_HEIGHT)
