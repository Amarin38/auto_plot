from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from infrastructure import DBBase


class DistribucionNormalModel(DBBase):
    __tablename__ = "DISTRIBUCION_NORMAL"

    id:                 Mapped[int] = mapped_column(primary_key=True)
    Años:               Mapped[int]
    Cambio:             Mapped[int]
    Cabecera:           Mapped[str] = mapped_column(nullable=True)
    Repuesto:           Mapped[str]
    TipoRepuesto:       Mapped[str]
    AñoPromedio:        Mapped[float]
    DesviacionEstandar: Mapped[float]
    DistribucionNormal: Mapped[str] = mapped_column(nullable=True)