from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from ... import ServicesBase

class ForecastModel(ServicesBase):
    __tablename__ = "forecast"
    
    id:                 Mapped[int] = mapped_column(primary_key=True)
    Repuesto:           Mapped[str]
    TipoRepuesto:       Mapped[str]
    Mes:                Mapped[int]
    Prevision:          Mapped[int]
    TotalPrevision:     Mapped[int]         