from sqlalchemy import String
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column, relationship
from typing import List

from ... import CommonBase

class CilindrosModel(CommonBase):
    __tablename__ = "cilindrada"
    
    id:           Mapped[int] = mapped_column(primary_key=True)
    Cilindros:    Mapped[str] = mapped_column(String(2))
    
    Motores:      Mapped[List["MotoresModel"]] = relationship(back_populates="Cilindrada") # type: ignore