from sqlalchemy import String, DECIMAL
from sqlalchemy.orm import Mapped, mapped_column
from infrastructure import DBBase
from decimal import Decimal

class MaximosMinimosModel(DBBase):
    __tablename__ = "MAXIMOS_MINIMOS"

    id:         Mapped[int] = mapped_column(primary_key=True)
    Familia:    Mapped[int]
    Articulo:   Mapped[int]
    Repuesto:   Mapped[str] = mapped_column(String(150), index=True)
    Minimo:     Mapped[Decimal] = mapped_column(DECIMAL(10,2))
    Maximo:     Mapped[Decimal] = mapped_column(DECIMAL(10,2))