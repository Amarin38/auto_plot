from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column
from infrastructure import dbbase_sqlite


class GomeriaTransferenciasEntreDepModel(dbbase_sqlite):
    __tablename__ = "stats_gomeria_transferencias_dep"

    id:         Mapped[int] = mapped_column(primary_key=True)
    Repuesto:   Mapped[str] = mapped_column(String(150), index=True)
    Año:        Mapped[int]
    Cantidad:   Mapped[int]
    Cabecera:   Mapped[str] = mapped_column(String(40), index=True)
