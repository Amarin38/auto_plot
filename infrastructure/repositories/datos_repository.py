from infrastructure.repositories.base_repository import BaseRepository

from domain.entities.datos.coches_cabecera import CochesCabecera
from domain.entities.datos.maximos_minimos import MaximosMinimos
from domain.entities.datos.parque_movil import ParqueMovil
from domain.entities.datos.proveedores import Proveedores
from domain.entities.datos.repuestos_codigos import RepuestosCodigos
from domain.entities.datos.usuarios_codigos import UsuariosCodigos
from domain.entities.json_config import JSONConfig
from domain.entities.usuario import UserAuth
from infrastructure.models import CochesCabeceraModel, MaximosMinimosModel, ParqueMovilModel, ProveedoresModel, \
    RepuestosCodigosModel, UsuariosCodigosModel, JSONConfigModel, UserAuthModel


class CochesCabeceraRepository(BaseRepository[CochesCabecera, CochesCabeceraModel]):
    entity_cls = CochesCabecera
    model_cls = CochesCabeceraModel

class MaximosMinimosRepository(BaseRepository[MaximosMinimos, MaximosMinimosModel]):
    entity_cls = MaximosMinimos
    model_cls = MaximosMinimosModel

class ParqueMovilRepository(BaseRepository[ParqueMovil, ParqueMovilModel]):
    entity_cls = ParqueMovil
    model_cls = ParqueMovilModel

class ProveedoresRepository(BaseRepository[Proveedores, ProveedoresModel]):
    entity_cls = Proveedores
    model_cls = ProveedoresModel

class RepuestosCodigosRepository(BaseRepository[RepuestosCodigos, RepuestosCodigosModel]):
    entity_cls = RepuestosCodigos
    model_cls = RepuestosCodigosModel

class UsuariosCodigosRepository(BaseRepository[UsuariosCodigos, UsuariosCodigosModel]):
    entity_cls = UsuariosCodigos
    model_cls = UsuariosCodigosModel

class JSONConfigRepository(BaseRepository[JSONConfig, JSONConfigModel]):
    entity_cls = JSONConfig
    model_cls = JSONConfigModel

class UsuarioRepository(BaseRepository[UserAuth, UserAuthModel]):
    entity_cls = UserAuth
    model_cls = UserAuthModel
