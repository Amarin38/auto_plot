from datetime import datetime

from sqlalchemy import Integer, String
from sqlalchemy import DateTime

from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

from ... import ServicesBase

class DatosGarantiasModel(ServicesBase):
    __tablename__ = "datos_garantias"

    id:                 Mapped[int] = mapped_column(primary_key=True)
    Año:                Mapped[int]
    Mes:                Mapped[str]
    FechaIngreso:       Mapped[datetime] = mapped_column(DateTime, nullable=True)
    FechaEnvio:         Mapped[datetime] = mapped_column(DateTime, nullable=True)
    Cabecera:           Mapped[str]
    Interno:            Mapped[int]
    Codigo:             Mapped[str]
    Repuesto:           Mapped[str]
    Cantidad:           Mapped[int]
    FechaColocacion:    Mapped[datetime] = mapped_column(DateTime, nullable=True)
    Detalle:            Mapped[str] = mapped_column(String, nullable=True)
    Tipo:               Mapped[str]
    DiasColocado:       Mapped[int] = mapped_column(Integer, nullable=True)
