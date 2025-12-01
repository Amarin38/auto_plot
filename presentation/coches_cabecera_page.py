import streamlit as st
from config.constants_views import PAG_COCHES_CABECERA
from viewmodels.common.coches_cabecera_vm import CochesCabeceraVM


def coches_cabecera():
    st.title(PAG_COCHES_CABECERA)

    st.dataframe(CochesCabeceraVM().get_df())