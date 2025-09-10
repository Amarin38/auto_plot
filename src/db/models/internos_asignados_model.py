from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from .. import Base

class InternosAsignados(Base):
    __tablename__ = "internos_asignados"
    
    id:             Mapped[int] = mapped_column(primary_key=True)
    Linea:          Mapped[int]
    Interno:        Mapped[int]
    Dominio:        Mapped[str]
    ChasisModelo:   Mapped[str]
    ChasisNum:      Mapped[str]
    ChasisAño:      Mapped[int]
    MotorModelo:    Mapped[str]
    MotorNumSerie:  Mapped[int]
    Cabecera:       Mapped[str]
