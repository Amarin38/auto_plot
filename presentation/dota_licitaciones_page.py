import streamlit as st

from config.constants_common import LICITACIONES_URL


def dota_licitaciones_page():
    st.markdown(
        """
        <meta http-equiv="refresh" content="0; url='{licitaciones}'" />
        """.format(licitaciones=LICITACIONES_URL),
        unsafe_allow_html=True
    )
