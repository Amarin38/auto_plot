from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from infrastructure import ServicesBase

class MaximosMinimosModel(ServicesBase):
    __tablename__ = "maximos_minimos"
    
    id:         Mapped[int] = mapped_column(primary_key=True)
    Familia:    Mapped[int]
    Articulo:   Mapped[int]
    Repuesto:   Mapped[str]
    Minimo:     Mapped[float]
    Maximo:     Mapped[float]