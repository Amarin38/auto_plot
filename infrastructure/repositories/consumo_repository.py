from domain.entities.consumo.prevision import ConsumoPrevision
from infrastructure.repositories.base_repository import BaseRepository

from domain.entities.consumo.comparacion import ConsumoComparacion
from domain.entities.consumo.desviacion_indices import ConsumoDesviacionIndices
from domain.entities.consumo.distribucion_normal import DistribucionNormal
from domain.entities.consumo.duracion_repuestos import DuracionRepuestos
from domain.entities.consumo.historial import ConsumoHistorial
from domain.entities.consumo.indice import ConsumoIndice
from domain.entities.consumo.obligatorio import ConsumoObligatorio
from domain.entities.consumo.prevision_data import ConsumoPrevisionData
from domain.entities.inicio_conteo_stock import ConteoStock
from infrastructure.db.models import ConsumoComparacionModel, ConsumoDesviacionIndicesModel, DistribucionNormalModel, \
    DuracionRepuestosModel, ConsumoHistorialModel, ConsumoIndiceModel, ConteoStockModel, ConsumoObligatorioModel, \
    ConsumoPrevisionDataModel, ConsumoPrevisionModel


class ConsumoComparacionRepository(BaseRepository[ConsumoComparacion, ConsumoComparacionModel]):
    entity_cls = ConsumoComparacion
    model_cls = ConsumoComparacionModel

class ConsumoDesviacionIndicesRepository(BaseRepository[ConsumoDesviacionIndices, ConsumoDesviacionIndicesModel]):
    entity_cls = ConsumoDesviacionIndices
    model_cls = ConsumoDesviacionIndicesModel

class DistribucionNormalRepository(BaseRepository[DistribucionNormal, DistribucionNormalModel]):
    entity_cls = DistribucionNormal
    model_cls = DistribucionNormalModel

class DuracionRepuestosRepository(BaseRepository[DuracionRepuestos, DuracionRepuestosModel]):
    entity_cls = DuracionRepuestos
    model_cls = DuracionRepuestosModel

class ConsumoHistorialRepository(BaseRepository[ConsumoHistorial, ConsumoHistorialModel]):
    entity_cls = ConsumoHistorial
    model_cls = ConsumoHistorialModel

class ConsumoIndiceRepository(BaseRepository[ConsumoIndice, ConsumoIndiceModel]):
    entity_cls = ConsumoIndice
    model_cls = ConsumoIndiceModel

class ConteoStockRepository(BaseRepository[ConteoStock, ConteoStockModel]):
    entity_cls = ConteoStock
    model_cls = ConteoStockModel

class ConsumoObligatorioRepository(BaseRepository[ConsumoObligatorio, ConsumoObligatorioModel]):
    entity_cls = ConsumoObligatorio
    model_cls = ConsumoObligatorioModel

class ConsumoPrevisionDataRepository(BaseRepository[ConsumoPrevisionData, ConsumoPrevisionDataModel]):
    entity_cls = ConsumoPrevisionData
    model_cls = ConsumoPrevisionDataModel

class ConsumoPrevisionRepository(BaseRepository[ConsumoPrevision, ConsumoPrevisionModel]):
    entity_cls = ConsumoPrevision
    model_cls = ConsumoPrevisionModel

