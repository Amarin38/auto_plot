from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from infrastructure import DBBase


class CochesCabeceraModel(DBBase):
    __tablename__ = "COCHES_CABECERA"
    
    id:                 Mapped[int] = mapped_column(primary_key=True)
    Cabecera:           Mapped[str]
    CochesDuermen:      Mapped[int] = mapped_column(nullable=True)
    CochesDuermenNuevo: Mapped[int] = mapped_column(nullable=True)
    CochesSinScania:    Mapped[int] = mapped_column(nullable=True)