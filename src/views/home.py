import sys, os

import streamlit as st

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
from src.db import Base, engine

from src.views.index_view import IndexPage
from src.views.forecast_view import ForecastPage
from src.views.maxmin_view import MaxminPage

def main():
    st.title("Estadisticas repuestos")
    st.set_page_config(
        page_title="Estadisticas",
        page_icon="📊",
        layout="wide",
        )
    
    main, indices, prevision, maxmins = st.tabs(["Página principal", "Índices de consumo", "Previsión de consumo", "Máximos y Mínimos"])


    with main:
        st.text("Pagina principal")
    with indices:
        IndexPage().indice_options()
    with prevision:
        ForecastPage().prevision_options()
    with maxmins:
        MaxminPage().show_table()

    # col1, col2, col3 = st.columns([1, 1.2, 10], vertical_alignment="center", gap="small")
    
    # inicializo el estado del boton 
    # if "active_page" not in st.session_state:
    #     st.session_state.active_page = None


    # mantengo activos los botones
    # if col1.button("Indices"):
    #     st.session_state.active_page = "indice"
    
    # if col2.button("Prevision"):
    #     st.session_state.active_page = "prevision" 

    # if col3.button("Maximos y Minimos"):
    #     st.session_state.active_page = "maxmin"

    # dependiendo de cual se active hace una cosa u otra
    

    # match(st.session_state.active_page):
    #     case "indice": indice.indice_options()
    #     case "prevision": tendencia.tendencia_options()
    #     case "maxmin": maxmin.show_table()
    

if __name__ == "__main__":
    Base.metadata.create_all(engine)
    main()