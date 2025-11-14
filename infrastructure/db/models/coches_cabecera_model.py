from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from infrastructure import DBBase


class CochesCabeceraModel(DBBase):
    __tablename__ = "COCHES_CABECERA"
    
    id:                 Mapped[int] = mapped_column(primary_key=True)
    Cabecera:           Mapped[str]
    CantidadCoches:     Mapped[int] = mapped_column(nullable=True)
    CantidadCochesNew:  Mapped[int] = mapped_column(nullable=True)
