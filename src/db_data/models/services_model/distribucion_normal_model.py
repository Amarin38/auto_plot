from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from ... import ServicesBase

class DistribucionNormalModel(ServicesBase):
    __tablename__ = 'distribucion_normal'

    id:                 Mapped[int] = mapped_column(primary_key=True)
    Años:               Mapped[int]
    Cambio:             Mapped[int]
    Repuesto:           Mapped[str]
    TipoRepuesto:       Mapped[str]
    AñoPromedio:        Mapped[float]
    DesviacionEstandar: Mapped[float]
    DistribucionNormal: Mapped[str]