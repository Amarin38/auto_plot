import sys, os

import streamlit as st

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
from src.db_data import CommonBase, ServicesBase
from src.db_data import common_engine, services_engine

from src.views.index_view import index_page
from src.views.forecast_view import forecast_page
from src.views.deviation_view import deviation_page
from src.views.maxmin_view import maxmin_page

from src.views.sidebar_view import LoadDataSideBar
from src.views.falla_equipos_garantia_view import falla_equipos_garantias_page

from src.config.constants import MAIN_TABS, LINK_BOX_HEIGHT, LINK_BOX_WIDTH

# Services DB -----------------------------------------------------------------------------------

# Common DB -----------------------------------------------------------------------------------

# -----------------------------------------------------------------------------------------------


def main():
    st.title("Estadisticas repuestos")
    st.set_page_config(
        page_title="Estadisticas",
        page_icon="📊",
        layout="wide",
        initial_sidebar_state="collapsed"
        )
    
    main_page, indices, prevision, desviacion, falla_garantias, maxmins = st.tabs(MAIN_TABS)

    LoadDataSideBar().select_data()

    with (main_page):
        st.text("Páginas de la empresa:")

        with st.container(height=LINK_BOX_HEIGHT, width=LINK_BOX_WIDTH):
            flota, licitaciones = st.columns(2)

            flota.link_button("SISSSA FLOTA", "https://sistemasanantonio.com.ar/flota/login.aspx")
            licitaciones.link_button("Dota Licitaciones", "https://dota.sistemasanantonio.com.ar/licitaciones/index.aspx")

    with indices:
        index_page()
    with prevision:
        forecast_page()
    with desviacion:
        deviation_page()
    with falla_garantias:
        falla_equipos_garantias_page()
    with maxmins:
        maxmin_page()


if __name__ == "__main__":
    CommonBase.metadata.create_all(common_engine)
    ServicesBase.metadata.create_all(services_engine)

    main()