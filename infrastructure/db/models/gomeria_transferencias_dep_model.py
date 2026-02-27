from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column
from infrastructure import DBBase
from infrastructure.db.models.base_model_mixin import BaseModelMixin, BaseRepuesto


class GomeriaTransferenciasEntreDepModel(BaseModelMixin, BaseRepuesto, DBBase):
    __tablename__ = "GOMERIA_TRANSFERENCIAS_DEP"

    Año: Mapped[int]
    Cantidad: Mapped[int]
    Cabecera: Mapped[str] = mapped_column(String(40), index=True)
