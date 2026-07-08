from sqlalchemy.orm import Session
from typing import Type, Optional, Dict
from infrastructure import session_sqlite_db

from infrastructure.repositories.consumo_repository import ConteoStockRepository, ConsumoIndiceRepository, \
    ConsumoHistorialRepository, ConsumoPrevisionRepository, DuracionRepuestosRepository, ConsumoComparacionRepository, \
    ConsumoObligatorioRepository, DistribucionNormalRepository, ConsumoPrevisionDataRepository, \
    ConsumoDesviacionIndicesRepository

from infrastructure.repositories.datos_repository import UsuarioRepository, JSONConfigRepository, ParqueMovilRepository, \
    CochesCabeceraRepository, MaximosMinimosRepository, UsuariosCodigosRepository, RepuestosCodigosRepository, \
    ProveedoresRepository

from infrastructure.repositories.garantias_repository import GarantiasDatosRepository, GarantiasFallaRepository, \
    GarantiasConsumoRepository

from infrastructure.repositories.gomeria_repository import GomeriaDiferenciaMovEntreDepRepository, \
    GomeriaTransferenciasEntreDepRepository


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

    @property
    def usuarios_codigos(self) -> UsuariosCodigosRepository:
        raise NotImplementedError

    @property
    def repuestos_codigos(self) -> RepuestosCodigosRepository:
        raise NotImplementedError

    @property
    def proveedor(self) -> ProveedoresRepository:
        raise NotImplementedError


class SQLAlchemyUnitOfWork(AbstractUnitOfWork):
    REPOSITORY_MAP: Dict[str, Type] = {
        "usuario": UsuarioRepository,
        "json_config": JSONConfigRepository,
        "conteo_stock": ConteoStockRepository,
        "parque_movil": ParqueMovilRepository,
        "consumo_indice": ConsumoIndiceRepository,
        "coches_cabecera": CochesCabeceraRepository,
        "garantias_datos": GarantiasDatosRepository,
        "garantias_falla": GarantiasFallaRepository,
        "maximos_minimos": MaximosMinimosRepository,
        "usuarios_codigos": UsuariosCodigosRepository,
        "consumo_historial": ConsumoHistorialRepository,
        "consumo_prevision": ConsumoPrevisionRepository,
        "garantias_consumo": GarantiasConsumoRepository,
        "duracion_repuestos": DuracionRepuestosRepository,
        "consumo_comparacion": ConsumoComparacionRepository,
        "consumo_obligatorio": ConsumoObligatorioRepository,
        "distribucion_normal": DistribucionNormalRepository,
        "consumo_prevision_data": ConsumoPrevisionDataRepository,
        "consumo_desviacion_indices": ConsumoDesviacionIndicesRepository,
        "gomeria_diferencia_mov": GomeriaDiferenciaMovEntreDepRepository,
        "gomeria_transferencias": GomeriaTransferenciasEntreDepRepository,
        "repuestos_codigos": RepuestosCodigosRepository,
        "proveedor": ProveedoresRepository,
    }

    def __init__(self, session_factory: Type[Session] = session_sqlite_db):
        self.session_factory = session_factory
        self._session: Optional[Session] = None
        self._repos: Dict[str, object] = {}

    def __enter__(self) -> 'SQLAlchemyUnitOfWork':
        self._session = self.session_factory()
        self._repos = {
            name: repo_cls(self._session)
            for name, repo_cls in self.REPOSITORY_MAP.items()
        }
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
        return self._repos["usuario"]

    @property
    def json_config(self) -> JSONConfigRepository:
        return self._repos["json_config"]

    @property
    def conteo_stock(self) -> ConteoStockRepository:
        return self._repos["conteo_stock"]

    @property
    def parque_movil(self) -> ParqueMovilRepository:
        return self._repos["parque_movil"]

    @property
    def consumo_indice(self) -> ConsumoIndiceRepository:
        return self._repos["consumo_indice"]

    @property
    def coches_cabecera(self) -> CochesCabeceraRepository:
        return self._repos["coches_cabecera"]

    @property
    def garantias_datos(self) -> GarantiasDatosRepository:
        return self._repos["garantias_datos"]

    @property
    def garantias_falla(self) -> GarantiasFallaRepository:
        return self._repos["garantias_falla"]

    @property
    def maximos_minimos(self) -> MaximosMinimosRepository:
        return self._repos["maximos_minimos"]

    @property
    def consumo_historial(self) -> ConsumoHistorialRepository:
        return self._repos["consumo_historial"]

    @property
    def consumo_prevision(self) -> ConsumoPrevisionRepository:
        return self._repos["consumo_prevision"]

    @property
    def garantias_consumo(self) -> GarantiasConsumoRepository:
        return self._repos["garantias_consumo"]

    @property
    def duracion_repuestos(self) -> DuracionRepuestosRepository:
        return self._repos["duracion_repuestos"]

    @property
    def consumo_comparacion(self) -> ConsumoComparacionRepository:
        return self._repos["consumo_comparacion"]

    @property
    def consumo_obligatorio(self) -> ConsumoObligatorioRepository:
        return self._repos["consumo_obligatorio"]

    @property
    def distribucion_normal(self) -> DistribucionNormalRepository:
        return self._repos["distribucion_normal"]

    @property
    def consumo_prevision_data(self) -> ConsumoPrevisionDataRepository:
        return self._repos["consumo_prevision_data"]

    @property
    def consumo_desviacion_indices(self) -> ConsumoDesviacionIndicesRepository:
        return self._repos["consumo_desviacion_indices"]

    @property
    def gomeria_diferencia_mov(self) -> GomeriaDiferenciaMovEntreDepRepository:
        return self._repos["gomeria_diferencia_mov"]

    @property
    def gomeria_transferencias(self) -> GomeriaTransferenciasEntreDepRepository:
        return self._repos["gomeria_transferencias"]

    @property
    def usuarios_codigos(self) -> UsuariosCodigosRepository:
        return self._repos["usuarios_codigos"]

    @property
    def repuestos_codigos(self) -> RepuestosCodigosRepository:
        return self._repos["repuestos_codigos"]

    @property
    def proveedor(self) -> ProveedoresRepository:
        return self._repos["proveedor"]