from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from infrastructure import DBBase
from infrastructure.db.models.base_model_mixin import BaseModelMixin


class GarantiasFallaModel(DBBase, BaseModelMixin):
    __tablename__ = "GARANTIAS_FALLA"

    Cabecera:               Mapped[str]
    Repuesto:               Mapped[str]
    TipoRepuesto:           Mapped[str] = mapped_column(nullable=True)
    PromedioTiempoFalla:    Mapped[int]
