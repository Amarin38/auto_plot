from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from infrastructure import DBBase


class MaximosMinimosModel(DBBase):
    __tablename__ = "MAXIMOS_MINIMOS"
    
    id:         Mapped[int] = mapped_column(primary_key=True)
    Familia:    Mapped[int]
    Articulo:   Mapped[int]
    Repuesto:   Mapped[str]
    Minimo:     Mapped[float]
    Maximo:     Mapped[float]