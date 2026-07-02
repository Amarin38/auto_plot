from decimal import Decimal
from sqlalchemy import String, DECIMAL
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from infrastructure import DBBase


class GomeriaDiferenciaMovEntreDepModel(DBBase):
    __tablename__ = "GOMERIA_DIFERENCIA_MOV_DEP"

    id:                 Mapped[int] = mapped_column(primary_key=True)
    Familia:            Mapped[int]
    Articulo:           Mapped[int]
    Repuesto:           Mapped[str] = mapped_column(String(150), index=True)
    Cantidad2024:       Mapped[int]
    CostoTotal2024:     Mapped[Decimal] = mapped_column(DECIMAL(10,2))
    Cantidad2025:       Mapped[int]
    CostoTotal2025:     Mapped[Decimal] = mapped_column(DECIMAL(10,2))
    DiferenciaAnual:    Mapped[int]
    DiferenciaDeCostos: Mapped[Decimal] = mapped_column(DECIMAL(10,2), nullable=True)
