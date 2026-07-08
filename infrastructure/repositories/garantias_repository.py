from infrastructure.repositories.base_repository import BaseRepository

from domain.entities.garantias.consumo import GarantiasConsumo
from domain.entities.garantias.datos import GarantiasDatos
from domain.entities.garantias.falla import GarantiasFalla
from infrastructure.db.models import GarantiasConsumoModel, GarantiasDatosModel, GarantiasFallaModel


class GarantiasConsumoRepository(BaseRepository[GarantiasConsumo, GarantiasConsumoModel]):
    entity_cls = GarantiasConsumo
    model_cls = GarantiasConsumoModel

class GarantiasDatosRepository(BaseRepository[GarantiasDatos, GarantiasDatosModel]):
    entity_cls = GarantiasDatos
    model_cls = GarantiasDatosModel

class GarantiasFallaRepository(BaseRepository[GarantiasFalla, GarantiasFallaModel]):
    entity_cls = GarantiasFalla
    model_cls = GarantiasFallaModel

