from typing import Optional

from streamlit_authenticator.utilities.hasher import Hasher
from config.enums import RoleEnum
from domain.entities.usuario import Usuario
from infrastructure.repositories.usuario_repository import UsuarioRepository


class UsuarioVM:
    def __init__(self) -> None:
        self.repo = UsuarioRepository()

    def save_user(self, nombre: str, contraseña: str, rol: RoleEnum) -> None:
        contraseña_hasheada = Hasher().hash(contraseña)
        usuario = Usuario(nombre, contraseña_hasheada, rol)

        self.repo.insert_many(usuario)


    def get_credentials_by_name(self, nombre: str) -> Optional[tuple[dict, str]]:
        user = self.repo.get_by_nombre(nombre)
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
        users = self.repo.get_all()
        credentials = {"usernames": {}}

        for user in users:
            credentials["usernames"].update({
                    user.Nombre: {
                        "name": user.Nombre,
                        "password": user.Contraseña
                    }
                })

        return credentials

