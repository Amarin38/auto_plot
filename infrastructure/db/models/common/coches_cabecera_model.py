from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from infrastructure import CommonBase

class CochesCabeceraModel(CommonBase):
    __tablename__ = "coches_cabecera"
    
    id:                 Mapped[int] = mapped_column(primary_key=True)
    Cabecera:           Mapped[str]
    CantidadCoches:     Mapped[int] = mapped_column(nullable=True)
    CantidadCochesNew:  Mapped[int] = mapped_column(nullable=True)
