from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from infrastructure import DBBase
from infrastructure.db.models.base_model_mixin import BaseModelMixin, BaseCabecera


class GarantiasFallaModel(BaseModelMixin, BaseCabecera, DBBase):
    __tablename__ = "GARANTIAS_FALLA"

    Repuesto:               Mapped[str]
    TipoRepuesto:           Mapped[str] = mapped_column(nullable=True)
    PromedioTiempoFalla:    Mapped[int]
