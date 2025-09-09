from datetime import date
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy import Date
from . import Base

class ForecastTrend(Base):
    __tablename__ = "forecast_trend"
    
    id:                      Mapped[int] = mapped_column(primary_key=True)
    Repuesto:                Mapped[str]
    TipoRepuesto:            Mapped[str]
    FechaCompleta:           Mapped[str]
    Año:                     Mapped[int]
    Mes:                     Mapped[int]
    Tendencia:               Mapped[float]
    TendenciaEstacional:     Mapped[float]

    


