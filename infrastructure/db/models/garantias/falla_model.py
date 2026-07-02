from sqlalchemy import String
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from infrastructure import DBBase


class GarantiasFallaModel(DBBase):
    __tablename__ = "GARANTIAS_FALLA"

    id:                     Mapped[int] = mapped_column(primary_key=True)
    Cabecera:               Mapped[str] = mapped_column(String(40), index=True)
    Repuesto:               Mapped[str] = mapped_column(String(150), index=True)
    TipoRepuesto:           Mapped[str] = mapped_column(nullable=True)
    PromedioTiempoFalla:    Mapped[int]
