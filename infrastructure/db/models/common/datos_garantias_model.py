from datetime import datetime

from sqlalchemy import Integer, String
from sqlalchemy import DateTime

from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

from infrastructure import CommonBase

class DatosGarantiasModel(CommonBase):
    __tablename__ = "datos_garantias"

    id:                 Mapped[int] = mapped_column(primary_key=True)
    Año:                Mapped[int] = mapped_column(Integer, nullable=True)
    Mes:                Mapped[str] = mapped_column(String, nullable=True)
    FechaIngreso:       Mapped[datetime] = mapped_column(DateTime, nullable=True)
    FechaEnvio:         Mapped[datetime] = mapped_column(DateTime, nullable=True)
    Cabecera:           Mapped[str]
    Interno:            Mapped[int] = mapped_column(nullable=True)
    Codigo:             Mapped[str]
    Repuesto:           Mapped[str]
    Cantidad:           Mapped[int] = mapped_column(nullable=True)
    FechaColocacion:    Mapped[datetime] = mapped_column(DateTime, nullable=True)
    Detalle:            Mapped[str] = mapped_column(String, nullable=True)
    Tipo:               Mapped[str]
    DiasColocado:       Mapped[int] = mapped_column(Integer, nullable=True)
