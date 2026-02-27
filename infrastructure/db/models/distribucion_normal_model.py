from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from infrastructure import DBBase
from infrastructure.db.models.base_model_mixin import BaseModelMixin


class DistribucionNormalModel(BaseModelMixin, DBBase):
    __tablename__ = "DISTRIBUCION_NORMAL"

    Años:               Mapped[int]
    Cambio:             Mapped[int]
    Cabecera:           Mapped[str] = mapped_column(nullable=True)
    Repuesto:           Mapped[str]
    TipoRepuesto:       Mapped[str]
    AñoPromedio:        Mapped[float]
    DesviacionEstandar: Mapped[float]
    DistribucionNormal: Mapped[str] = mapped_column(nullable=True)