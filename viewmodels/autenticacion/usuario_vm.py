from typing import Optional

from streamlit_authenticator.utilities.hasher import Hasher
from config.enums import RoleEnum
from domain.entities.usuario import Usuario
from infrastructure.unit_of_work import SQLAlchemyUnitOfWork


class UsuarioVM:
    def __init__(self, uow: SQLAlchemyUnitOfWork = SQLAlchemyUnitOfWork()) -> None:
        self.uow = uow

    def save_user(self, nombre: str, contraseña: str, rol: RoleEnum) -> None:
        contraseña_hasheada = Hasher().hash(contraseña)
        usuario = Usuario(nombre, contraseña_hasheada, rol)

        with self.uow as uow:
            uow.usuario.insert_many([usuario])


    def get_by_name(self, nombre: str) -> Usuario:
        with self.uow as uow:
            return uow.usuario.get_by_nombre(nombre)


    def get_credentials_by_name(self, nombre: str) -> Optional[tuple[dict, str]]:
        with self.uow as uow:
            user = uow.usuario.get_by_nombre(nombre)
            credentials = {
                "usernames": {
                    user.Nombre: {
                        "name": user.Nombre,
                        "password": user.Contraseña
                    }
                }
            }
            return credentials, user.Rol


    def get_credentials(self) -> Optional[dict]:
        with self.uow as uow:
            users = uow.usuario.get_all()
            credentials = {"usernames": {}}

            for user in users:
                credentials["usernames"].update({
                        user.Nombre: {
                            "name": user.Nombre,
                            "password": user.Contraseña
                        }
                    })

            return credentials

