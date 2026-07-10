from typing import Optional

from domain.entities.datos.usuario import UserAuth
from viewmodels.base_vm import BaseVM


class UserAuthVM(BaseVM[UserAuth]):
    def __init__(self) -> None:
        columns_df = list(UserAuth.model_fields.keys())
        super().__init__(UserAuth, "usuario", columns_df)


    def get_by_name(self, name: str) -> UserAuth:
        return self.get_entity_by_filters({"Nombre": name})[0]


    def get_credentials_by_name(self, name: str) -> Optional[tuple[dict, str]]:
        user = self.get_by_name(name)

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
        users = self.get_entity()
        credentials = {"usernames": {}}

        for user in users:
            credentials["usernames"].update({
                user.Nombre: {
                    "name": user.Nombre,
                    "password": user.Contraseña
                }
            })

        return credentials