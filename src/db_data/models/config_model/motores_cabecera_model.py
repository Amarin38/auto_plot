from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from ... import CommonBase

class MotoresCabeceraModel(CommonBase):
    __tablename__ = "motores_cabecera"
    
    id:                Mapped[int] = mapped_column(primary_key=True)
    Cabecera:          Mapped[str]
    Motores:           Mapped[str]
    CantidadMotores:   Mapped[int]