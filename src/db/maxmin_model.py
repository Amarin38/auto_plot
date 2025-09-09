from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from . import Base

class Maxmin(Base):
    __tablename__ = "maxmin"
    
    id:         Mapped[int] = mapped_column(primary_key=True)
    Familia:    Mapped[int]
    Articulo:   Mapped[int]
    Repuesto:   Mapped[str]
    Minimo:     Mapped[float]
    Maximo:     Mapped[float]