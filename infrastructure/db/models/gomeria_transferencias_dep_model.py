from sqlalchemy.orm import Mapped
from infrastructure import DBBase
from infrastructure.db.models.base_model_mixin import BaseModelMixin


class GomeriaTransferenciasEntreDepModel(DBBase, BaseModelMixin):
    __tablename__ = "GOMERIA_TRANSFERENCIAS_DEP"

    Repuesto: Mapped[str]
    Año: Mapped[int]
    Cantidad: Mapped[int]
    Cabecera: Mapped[str]
