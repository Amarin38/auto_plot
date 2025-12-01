import streamlit as st

from config.constants_views import PAG_PARQUE_MOVIL


def parque_movil():
    st.title(PAG_PARQUE_MOVIL)

    # TODO: crear una base de datos donde guardar todas las flotas con su fecha de creacion incluida
    # TODO: agregar un buscador para traer todos los datos de cada consulta