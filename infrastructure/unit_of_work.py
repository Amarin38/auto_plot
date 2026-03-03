from sqlalchemy.orm import Session
from typing import Type, Optional
from infrastructure import SessionDB

from infrastructure.repositories.usuario_repository import UsuarioRepository
from infrastructure.repositories.json_config_repository import JSONConfigRepository
from infrastructure.repositories.conteo_stock_repository import ConteoStockRepository
from infrastructure.repositories.parque_movil_repository import ParqueMovilRepository
from infrastructure.repositories.consumo_indice_repository import ConsumoIndiceRepository
from infrastructure.repositories.coches_cabecera_repository import CochesCabeceraRepository
from infrastructure.repositories.garantias_datos_repository import GarantiasDatosRepository
from infrastructure.repositories.garantias_falla_repository import GarantiasFallaRepository
from infrastructure.repositories.maximos_minimos_repository import MaximosMinimosRepository
from infrastructure.repositories.consumo_historial_repository import ConsumoHistorialRepository
from infrastructure.repositories.consumo_prevision_repository import ConsumoPrevisionRepository
from infrastructure.repositories.garantias_consumo_repository import GarantiasConsumoRepository
from infrastructure.repositories.duracion_repuestos_repository import DuracionRepuestosRepository
from infrastructure.repositories.consumo_comparacion_repository import ConsumoComparacionRepository
from infrastructure.repositories.consumo_obligatorio_repository import ConsumoObligatorioRepository
from infrastructure.repositories.distribucion_normal_repository import DistribucionNormalRepository
from infrastructure.repositories.consumo_prevision_data_repository import ConsumoPrevisionDataRepository
from infrastructure.repositories.consumo_desviacion_indices_repository import ConsumoDesviacionIndicesRepository
from infrastructure.repositories.gomeria_diferencia_mov_dep_repository import GomeriaDiferenciaMovEntreDepRepository
from infrastructure.repositories.gomeria_transferencias_dep_repository import GomeriaTransferenciasEntreDepRepository


class AbstractUnitOfWork:
    def __enter__(self) -> 'AbstractUnitOfWork':
        raise NotImplementedError

    def __exit__(self, *args):
        self.rollback()

    def commit(self):
        raise NotImplementedError

    def rollback(self):
        raise NotImplementedError

    @property
    def usuario(self) -> UsuarioRepository:
        raise NotImplementedError

    @property
    def json_config(self) -> JSONConfigRepository:
        raise NotImplementedError

    @property
    def conteo_stock(self) -> ConteoStockRepository:
        raise NotImplementedError

    @property
    def parque_movil(self) -> ParqueMovilRepository:
        raise NotImplementedError

    @property
    def consumo_indice(self) -> ConsumoIndiceRepository:
        raise NotImplementedError

    @property
    def coches_cabecera(self) -> CochesCabeceraRepository:
        raise NotImplementedError

    @property
    def garantias_datos(self) -> GarantiasDatosRepository:
        raise NotImplementedError

    @property
    def garantias_falla(self) -> GarantiasFallaRepository:
        raise NotImplementedError

    @property
    def maximos_minimos(self) -> MaximosMinimosRepository:
        raise NotImplementedError

    @property
    def consumo_historial(self) -> ConsumoHistorialRepository:
        raise NotImplementedError

    @property
    def consumo_prevision(self) -> ConsumoPrevisionRepository:
        raise NotImplementedError

    @property
    def garantias_consumo(self) -> GarantiasConsumoRepository:
        raise NotImplementedError

    @property
    def duracion_repuestos(self) -> DuracionRepuestosRepository:
        raise NotImplementedError

    @property
    def consumo_comparacion(self) -> ConsumoComparacionRepository:
        raise NotImplementedError

    @property
    def consumo_obligatorio(self) -> ConsumoObligatorioRepository:
        raise NotImplementedError

    @property
    def distribucion_normal(self) -> DistribucionNormalRepository:
        raise NotImplementedError

    @property
    def consumo_prevision_data(self) -> ConsumoPrevisionDataRepository:
        raise NotImplementedError

    @property
    def consumo_desviacion_indices(self) -> ConsumoDesviacionIndicesRepository:
        raise NotImplementedError

    @property
    def gomeria_diferencia_mov(self) -> GomeriaDiferenciaMovEntreDepRepository:
        raise NotImplementedError

    @property
    def gomeria_transferencias(self) -> GomeriaTransferenciasEntreDepRepository:
        raise NotImplementedError


class SQLAlchemyUnitOfWork(AbstractUnitOfWork):
    def __init__(self, session_factory: Type[Session] = SessionDB):
        self.session_factory = session_factory
        self._session: Optional[Session] = None

        self._usuario: Optional[UsuarioRepository]                                      = None
        self._json_config: Optional[JSONConfigRepository]                               = None
        self._conteo_stock: Optional[ConteoStockRepository]                             = None
        self._parque_movil: Optional[ParqueMovilRepository]                             = None
        self._consumo_indice: Optional[ConsumoIndiceRepository]                         = None
        self._coches_cabecera: Optional[CochesCabeceraRepository]                       = None
        self._garantias_datos: Optional[GarantiasDatosRepository]                       = None
        self._garantias_fallas: Optional[GarantiasFallaRepository]                      = None
        self._maximos_minimos: Optional[MaximosMinimosRepository]                       = None
        self._consumo_historial: Optional[ConsumoHistorialRepository]                   = None
        self._consumo_prevision: Optional[ConsumoPrevisionRepository]                   = None
        self._garantias_consumo: Optional[GarantiasConsumoRepository]                   = None
        self._duracion_repuestos: Optional[DuracionRepuestosRepository]                 = None
        self._consumo_comparacion: Optional[ConsumoComparacionRepository]               = None
        self._consumo_obligatorio: Optional[ConsumoObligatorioRepository]               = None
        self._distribucion_normal: Optional[DistribucionNormalRepository]               = None
        self._consumo_prevision_data: Optional[ConsumoPrevisionDataRepository]          = None
        self._consumo_desviacion_indices: Optional[ConsumoDesviacionIndicesRepository]  = None
        self._gomeria_diferencia_mov: Optional[GomeriaDiferenciaMovEntreDepRepository]  = None
        self._gomeria_transferencias: Optional[GomeriaTransferenciasEntreDepRepository] = None

    def __enter__(self) -> 'SQLAlchemyUnitOfWork':
        self._session: Session = self.session_factory()

        self._usuario                   : Optional[UsuarioRepository] = UsuarioRepository(self._session)
        self._json_config               : Optional[JSONConfigRepository] = JSONConfigRepository(self._session)
        self._conteo_stock              : Optional[ConteoStockRepository] = ConteoStockRepository(self._session)
        self._parque_movil              : Optional[ParqueMovilRepository] = ParqueMovilRepository(self._session)
        self._consumo_indice            : Optional[ConsumoIndiceRepository]= ConsumoIndiceRepository(self._session)
        self._coches_cabecera           : Optional[CochesCabeceraRepository] = CochesCabeceraRepository(self._session)
        self._garantias_datos           : Optional[GarantiasDatosRepository] = GarantiasDatosRepository(self._session)
        self._garantias_fallas          : Optional[GarantiasFallaRepository] = GarantiasFallaRepository(self._session)
        self._maximos_minimos           : Optional[MaximosMinimosRepository] = MaximosMinimosRepository(self._session)
        self._consumo_historial         : Optional[ConsumoHistorialRepository] = ConsumoHistorialRepository(self._session)
        self._consumo_prevision         : Optional[ConsumoPrevisionRepository] = ConsumoPrevisionRepository(self._session)
        self._garantias_consumo         : Optional[GarantiasConsumoRepository] = GarantiasConsumoRepository(self._session)
        self._duracion_repuestos        : Optional[DuracionRepuestosRepository] = DuracionRepuestosRepository(self._session)
        self._consumo_comparacion       : Optional[ConsumoComparacionRepository] = ConsumoComparacionRepository(self._session)
        self._consumo_obligatorio       : Optional[ConsumoObligatorioRepository] = ConsumoObligatorioRepository(self._session)
        self._distribucion_normal       : Optional[DistribucionNormalRepository] = DistribucionNormalRepository(self._session)
        self._consumo_prevision_data    : Optional[ConsumoPrevisionDataRepository] = ConsumoPrevisionDataRepository(self._session)
        self._consumo_desviacion_indices: Optional[ConsumoDesviacionIndicesRepository]  = ConsumoDesviacionIndicesRepository(self._session)
        self._gomeria_diferencia_mov    : Optional[GomeriaDiferenciaMovEntreDepRepository]  = GomeriaDiferenciaMovEntreDepRepository(self._session)
        self._gomeria_transferencias    : Optional[GomeriaTransferenciasEntreDepRepository] = GomeriaTransferenciasEntreDepRepository(self._session)

        # Ejemplo:
        # from infrastructure.repositories.consumo_indice_repository import ConsumoIndiceRepository
        # self.consumo_indices = ConsumoIndiceRepository(self.session)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type:  # Si hubo una excepción, hacemos rollback
            self.rollback()
        else:  # Si no hubo excepción, intentamos confirmar si hay cambios
            try:
                # Comprobar si hay cambios pendientes (objetos nuevos, modificados o eliminados)
                if self._session.dirty or self._session.new or self._session.deleted:
                    self.commit()
                else:
                    # Si no hay cambios, hacemos rollback para cerrar la transacción limpiamente.
                    # Esto es inofensivo para operaciones de solo lectura y asegura que la transacción finalice.
                    self.rollback()
            except Exception as e:
                # Si el commit/rollback falla por alguna razón, aseguramos el rollback y relanzamos la excepción
                self.rollback()
                raise e
            finally:
                self._session.close()  # Siempre cierra la sesión al salir del bloque 'with'


    def commit(self):
        self._session.commit()

    def rollback(self):
        self._session.rollback()


    # implemento las propiedades para cada repositorio
    @property
    def usuario(self) -> UsuarioRepository:
        return self._usuario

    @property
    def json_config(self) -> JSONConfigRepository:
        return self._json_config

    @property
    def conteo_stock(self) -> ConteoStockRepository:
        return self._conteo_stock

    @property
    def parque_movil(self) -> ParqueMovilRepository:
        return self._parque_movil

    @property
    def consumo_indice(self) -> ConsumoIndiceRepository:
        return self._consumo_indice

    @property
    def coches_cabecera(self) -> CochesCabeceraRepository:
        return self._coches_cabecera

    @property
    def garantias_datos(self) -> GarantiasDatosRepository:
        return self._garantias_datos

    @property
    def garantias_falla(self) -> GarantiasFallaRepository:
        return self._garantias_fallas

    @property
    def maximos_minimos(self) -> MaximosMinimosRepository:
        return self._maximos_minimos

    @property
    def consumo_historial(self) -> ConsumoHistorialRepository:
        return self._consumo_historial

    @property
    def consumo_prevision(self) -> ConsumoPrevisionRepository:
        return self._consumo_prevision

    @property
    def garantias_consumo(self) -> GarantiasConsumoRepository:
        return self._garantias_consumo

    @property
    def duracion_repuestos(self) -> DuracionRepuestosRepository:
        return self._duracion_repuestos

    @property
    def consumo_comparacion(self) -> ConsumoComparacionRepository:
        return self._consumo_comparacion

    @property
    def consumo_obligatorio(self) -> ConsumoObligatorioRepository:
        return self._consumo_obligatorio

    @property
    def distribucion_normal(self) -> DistribucionNormalRepository:
        return self._distribucion_normal

    @property
    def consumo_prevision_data(self) -> ConsumoPrevisionDataRepository:
        return self._consumo_prevision_data

    @property
    def consumo_desviacion_indices(self) -> ConsumoDesviacionIndicesRepository:
        return self._consumo_desviacion_indices

    @property
    def gomeria_diferencia_mov(self) -> GomeriaDiferenciaMovEntreDepRepository:
        return self._gomeria_diferencia_mov

    @property
    def gomeria_transferencias(self) -> GomeriaTransferenciasEntreDepRepository:
        return self._gomeria_transferencias