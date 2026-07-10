import streamlit as st

from random import randint

from streamlit_authenticator import Hasher

from config.enums import RoleEnum
from config.constants_views import PAG_NUEVO_USUARIO, INPUT_HEIGHT, NUEVO_USUARIO_RADIO_HEIGHT
from domain.entities.datos.usuario import UserAuth
from presentation.streamlit_components import ButtonComponents
from viewmodels.auth_vm import UserAuthVM


def nuevo_usuario():
    buttons = ButtonComponents()

    aux1, centro, aux2 = st.columns([3,3,3])
    centro.title(PAG_NUEVO_USUARIO)

    with centro:
        _id: int = randint(0, 100)

        with st.container(height=INPUT_HEIGHT):
            nombre: str = st.text_input("Nombre")
        with st.container(height=INPUT_HEIGHT):
            contraseña: str = st.text_input("Contraseña")

        with st.container(height=NUEVO_USUARIO_RADIO_HEIGHT):
            rol: RoleEnum = st.radio("Selecciona el rol:", [RoleEnum.user, RoleEnum.admin],
                                     captions=["Usuario básico (solo ve estadisticas)",
                                               "Usuario administrador (puede ver y modificar)"])

        if nombre and contraseña and rol:
            creds = [format_credentials(nombre, contraseña, rol)]
            buttons.load_data_bttn(lambda: UserAuthVM().save(creds))


def format_credentials(nombre, contraseña, rol) -> UserAuth:
    contraseña_hasheada = Hasher().hash(contraseña)
    usuario = UserAuth(
        Nombre=nombre,
        Contraseña=contraseña_hasheada,
        Rol=rol
    )
    
    return usuario