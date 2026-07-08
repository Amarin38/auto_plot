from datetime import date
from sqlalchemy import Date, String
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from infrastructure import dbbase_sqlite


class ConsumoPrevisionModel(dbbase_sqlite):
    __tablename__ = "stats_consumo_prevision"

    id:                 Mapped[int] = mapped_column(primary_key=True)
    FechaCompleta:      Mapped[date] = mapped_column(Date)
    Prevision:          Mapped[int]
    Repuesto:           Mapped[str] = mapped_column(String(150), index=True)
    TipoRepuesto:       Mapped[str]
