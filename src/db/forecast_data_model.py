from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from . import Base

class ForecastData(Base):
    __tablename__ = "forecast_data"
    
    id:                 Mapped[int] = mapped_column(primary_key=True)
    Repuesto:           Mapped[str]
    TipoRepuesto:       Mapped[str]
    FechaCompleta:      Mapped[str]
    Año:                Mapped[int]
    Mes:                Mapped[int]
    TotalMes:           Mapped[int]
    Promedio:           Mapped[float]
    IndiceAnual:        Mapped[float]
    IndiceEstacional:   Mapped[float]        

    


