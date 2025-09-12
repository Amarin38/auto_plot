from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from .. import Base

class CochesCabeceraModel(Base):
    __tablename__ = "coches_cabecera"
    
    id:                 Mapped[int] = mapped_column(primary_key=True)
    Cabecera:           Mapped[str]
    CantidadCoches:     Mapped[int]
