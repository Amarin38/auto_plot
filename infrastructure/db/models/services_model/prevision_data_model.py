from datetime import date
from sqlalchemy import Date
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from infrastructure import ServicesBase

class PrevisionDataModel(ServicesBase):
    __tablename__ = "prevision_data"
    
    id:                 Mapped[int] = mapped_column(primary_key=True)
    FechaCompleta:      Mapped[date] = mapped_column(Date)
    Consumo:            Mapped[int]
    Repuesto:           Mapped[str]
    TipoRepuesto:       Mapped[str]
