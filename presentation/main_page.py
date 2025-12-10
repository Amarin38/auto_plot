import streamlit as st
from config.constants_views import LINK_BOX_HEIGHT, LINK_BOX_WIDTH, PAG_PRINCIPAL

def main():
    st.title(PAG_PRINCIPAL)
    st.text("Páginas de la empresa:")

    with st.container(height=LINK_BOX_HEIGHT, width=LINK_BOX_WIDTH):
        flota, licitaciones = st.columns([2, 2])

        flota_url = "https://sistemasanantonio.com.ar/san_antonio/mod_flota/Grilla_ParqueMovil.aspx"
        licitaciones_url = "https://dota.sistemasanantonio.com.ar/licitaciones/login.aspx"

        flota.link_button("SISSSA FLOTA", flota_url)
        licitaciones.link_button("Dota Licitaciones", licitaciones_url)