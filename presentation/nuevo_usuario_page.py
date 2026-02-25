import streamlit as st

from random import randint

from config.enums import RoleEnum
from config.constants_views import PAG_NUEVO_USUARIO, INPUT_HEIGHT, NUEVO_USUARIO_RADIO_HEIGHT
from viewmodels.autenticacion.usuario_vm import UsuarioVM
from presentation.streamlit_components import ButtonComponents, SelectBoxComponents


def nuevo_usuario():
    buttons = ButtonComponents()
    select = SelectBoxComponents()

    aux1, centro, aux2 = st.columns([3,3,3])
    centro.title(PAG_NUEVO_USUARIO)

    with centro:
        _id: int = randint(0, 100)

        with st.container(height=INPUT_HEIGHT):
            nombre: str = st.text_input("Nombre")
        with st.container(height=INPUT_HEIGHT):
            contraseña: str = st.text_input("Contraseña")

        with st.container(height=NUEVO_USUARIO_RADIO_HEIGHT):
            rol: RoleEnum = st.radio("Selecciona el rol:", [RoleEnum.USER, RoleEnum.ADMIN],
                                     captions=["Usuario básico (solo ve estadisticas)",
                                               "Usuario administrador (puede ver y modificar)"])

        if nombre and contraseña and rol:
            buttons.load_data_bttn(lambda: UsuarioVM().save_user(nombre, contraseña, rol))