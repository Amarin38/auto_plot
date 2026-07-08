from datetime import datetime
from sqlalchemy import Integer, String
from sqlalchemy import DateTime
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from infrastructure import dbbase_sqlite


class GarantiasDatosModel(dbbase_sqlite):
    __tablename__ = "stats_garantias_datos"

    id:                 Mapped[int]         = mapped_column(primary_key=True)
    Año:                Mapped[int]         = mapped_column(Integer, nullable=True)
    Mes:                Mapped[str]         = mapped_column(String, nullable=True)
    FechaIngreso:       Mapped[datetime]    = mapped_column(DateTime, nullable=True)
    FechaEnvio:         Mapped[datetime]    = mapped_column(DateTime, nullable=True)
    Cabecera:           Mapped[str]         = mapped_column(String(40), index=True)
    Interno:            Mapped[int]         = mapped_column(nullable=True)
    Codigo:             Mapped[str]
    Repuesto:           Mapped[str]         = mapped_column(String(150), index=True)
    Cantidad:           Mapped[int]         = mapped_column(nullable=True)
    FechaColocacion:    Mapped[datetime]    = mapped_column(DateTime, nullable=True)
    Detalle:            Mapped[str]         = mapped_column(String, nullable=True)
    Tipo:               Mapped[str]
    DiasColocado:       Mapped[int]         = mapped_column(Integer, nullable=True)
