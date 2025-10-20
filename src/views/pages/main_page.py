import streamlit as st

from src.config.constants import LINK_BOX_HEIGHT, LINK_BOX_WIDTH, PAG_PRINCIPAL


def main_page():
    st.title(PAG_PRINCIPAL)
    st.text("Páginas de la empresa:")

    with st.container(height=LINK_BOX_HEIGHT, width=LINK_BOX_WIDTH):
        flota, licitaciones = st.columns(2)

        flota.link_button("SISSSA FLOTA", "https://sistemasanantonio.com.ar/flota/login.aspx")
        licitaciones.link_button("Dota Licitaciones", "https://dota.sistemasanantonio.com.ar/licitaciones/index.aspx")