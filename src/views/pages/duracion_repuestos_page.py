import streamlit as st

from src.config.constants import PAG_DURACION
from src.utils.exception_utils import execute_safely


@execute_safely
def duracion_repuestos_page():
    st.title(PAG_DURACION)

