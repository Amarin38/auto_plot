from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from infrastructure import DBBase


class GarantiasFallaModel(DBBase):
    __tablename__ = "GARANTIAS_FALLA"

    id:                     Mapped[int] = mapped_column(primary_key=True)
    Cabecera:               Mapped[str]
    Repuesto:               Mapped[str]
    TipoRepuesto:           Mapped[str] = mapped_column(nullable=True)
    PromedioTiempoFalla:    Mapped[int]
