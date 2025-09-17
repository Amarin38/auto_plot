from sqlalchemy import String
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column, relationship
from typing import List

from ... import CommonBase

class ChasisModel(CommonBase):
    __tablename__ = "chasis"
    
    id:         Mapped[int] = mapped_column(primary_key=True)
    Modelo:     Mapped[str] = mapped_column(String(20))
    
    Motor:      Mapped[List["MotoresModel"]] = relationship(back_populates="chasis") # type: ignore
