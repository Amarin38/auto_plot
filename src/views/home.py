import sys, os

import streamlit as st

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
from src.views.index import IndexPage
from src.views.forecast import ForecastPage


def main():
    indice = IndexPage()
    tendencia = ForecastPage()

    st.title("Estadisticas repuestos")
    st.set_page_config(
        page_title="Estadisticas",
        page_icon="📊",
        layout="wide",
        )
    
    col1, col2 = st.columns([1, 8], vertical_alignment="center", gap="small")
    
    # inicializo el estado del boton 
    if "active_page" not in st.session_state:
        st.session_state.active_page = None

    # mantengo activos los botones
    if col1.button("Indices"):
        st.session_state.active_page = "indice"
    
    if col2.button("Tendencias"):
        st.session_state.active_page = "tendencia" 

    # dependiendo de cual se active hace una cosa u otra
    if st.session_state.active_page == "indice":
        indice.indice_options()
    elif st.session_state.active_page == "tendencia":
        tendencia.tendencia_options()
 

#TODO: agregar HTTPS para poder abrirlo en otra pc|

if __name__ == "__main__":
    main()