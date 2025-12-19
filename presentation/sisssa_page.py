import streamlit as st

from config.constants_common import FLOTA_URL


def sissa_page():
    st.markdown(
        """
        <meta http-equiv="refresh" content="0; url='{flota}'" />
        """.format(flota=FLOTA_URL),
        unsafe_allow_html=True
    )

