from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from ... import ServicesBase


class FallaGarantiasModel(ServicesBase):
    __tablename__ = "falla_garantias"

    id:                     Mapped[int] = mapped_column(primary_key=True)
    Cabecera:               Mapped[str]
    Repuesto:               Mapped[str]
    TipoRepuesto:           Mapped[str] = mapped_column(nullable=True)
    PromedioTiempoFalla:    Mapped[int]
