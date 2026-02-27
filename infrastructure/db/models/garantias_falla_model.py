from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from infrastructure import DBBase
from infrastructure.db.models.base_model_mixin import BaseModelMixin, BaseCabecera, BaseRepuesto


class GarantiasFallaModel(BaseModelMixin, BaseCabecera, BaseRepuesto, DBBase):
    __tablename__ = "GARANTIAS_FALLA"

    TipoRepuesto:           Mapped[str] = mapped_column(nullable=True)
    PromedioTiempoFalla:    Mapped[int]
