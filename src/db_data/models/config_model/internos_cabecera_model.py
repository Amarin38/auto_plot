from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from ... import CommonBase

class InternosCabeceraModel(CommonBase):
    __tablename__ = "internos_cabecera"
    
    id:         Mapped[int] = mapped_column(primary_key=True)
    Linea:      Mapped[int]
    Interno:    Mapped[int]
    Cabecera:   Mapped[str]
