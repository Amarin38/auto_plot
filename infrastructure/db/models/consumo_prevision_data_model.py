from datetime import date
from sqlalchemy import Date
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from infrastructure import DBBase


class ConsumoPrevisionDataModel(DBBase):
    __tablename__ = "CONSUMO_PREVISION_DATA"
    
    id:                 Mapped[int] = mapped_column(primary_key=True)
    FechaCompleta:      Mapped[date] = mapped_column(Date)
    Consumo:            Mapped[int]
    Repuesto:           Mapped[str]
    TipoRepuesto:       Mapped[str]
