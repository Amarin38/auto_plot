from sqlalchemy import String
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column, relationship
from typing import List

from ... import CommonBase

class NormativaModel(CommonBase):
    __tablename__ = "normativa"
    
    id:      Mapped[int] = mapped_column(primary_key=True)
    Euro:    Mapped[str] = mapped_column(String(2))
    
    Motores: Mapped[List["MotoresModel"]] = relationship(back_populates="Normativa") # type: ignore

