from infrastructure.repositories.base_repository import BaseRepository

from domain.entities.gomeria.diferencia_mov_dep import GomeriaDiferenciaMovEntreDep
from domain.entities.gomeria.movimientos import GomeriaMovimientos
from domain.entities.gomeria.transferencias_dep import GomeriaTransferenciasEntreDep
from infrastructure.models import GomeriaDiferenciaMovEntreDepModel, GomeriaTransferenciasEntreDepModel
from infrastructure.models.gomeria.movimientos_model import GomeriaMovimientosModel


class GomeriaMovimientosRepository(BaseRepository[GomeriaMovimientos, GomeriaMovimientosModel]):
    entity_cls = GomeriaMovimientos
    model_cls = GomeriaMovimientosModel

class GomeriaDiferenciaMovEntreDepRepository(BaseRepository[GomeriaDiferenciaMovEntreDep, GomeriaDiferenciaMovEntreDepModel]):
    entity_cls = GomeriaDiferenciaMovEntreDep
    model_cls = GomeriaDiferenciaMovEntreDepModel

class GomeriaTransferenciasEntreDepRepository(BaseRepository[GomeriaTransferenciasEntreDep, GomeriaTransferenciasEntreDepModel]):
    entity_cls = GomeriaTransferenciasEntreDep
    model_cls = GomeriaTransferenciasEntreDepModel