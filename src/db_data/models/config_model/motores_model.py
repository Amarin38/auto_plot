from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column, relationship

from ... import CommonBase

class MotoresModel(CommonBase):
    __tablename__ = "motor"
    
    id:           Mapped[int] = mapped_column(primary_key=True)
    Marca:        Mapped[str]
    Modelo:       Mapped[str]
    
    # Motor (M) --> (1) Normativa
    NormativaId:  Mapped[int] = mapped_column(ForeignKey("normativa.id"))
    Normativa:    Mapped["NormativaModel"] = relationship(back_populates="motor") # type: ignore


    # Motor (M) --> (1) MT
    ChasisId:     Mapped[int] = mapped_column(ForeignKey("chasis.id"))         
    Chasis:       Mapped["ChasisModel"] = relationship(back_populates="motor") # type: ignore
    

    # Motor (M) --> (1) Normativa
    CilindrosId:  Mapped[int] = mapped_column(ForeignKey("cilindrada.id"))
    Cilindro:     Mapped["CilindrosModel"] = relationship(back_populates="motor") # type: ignore


