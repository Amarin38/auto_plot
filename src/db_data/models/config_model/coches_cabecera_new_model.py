from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from ... import CommonBase


class CochesCabeceraNewModel(CommonBase):
    __tablename__ = "coches_cabecera_new"

    id:             Mapped[int] = mapped_column(primary_key=True)
    Cabecera:       Mapped[str]
    CantidadCoches: Mapped[int]
