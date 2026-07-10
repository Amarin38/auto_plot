from sqlalchemy import String
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from infrastructure import dbbase_sqlite


class GarantiasFallaModel(dbbase_sqlite):
    __tablename__ = "stats_garantias_falla"

    id:                     Mapped[int] = mapped_column(primary_key=True)
    Cabecera:               Mapped[str] = mapped_column(String(40), index=True)
    Repuesto:               Mapped[str] = mapped_column(String(150), index=True)
    TipoRepuesto:           Mapped[str] = mapped_column(nullable=True)
    PromedioTiempoFalla:    Mapped[int]
