from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from infrastructure import DBBase


class DiferenciaMovimientosEntreDepositosModel(DBBase):
    __tablename__ = "DIFERENCIA_MOV_DEP"

    id: Mapped[int] = mapped_column(primary_key=True)
    Familia: Mapped[int]
    Articulo: Mapped[int]
    Repuesto: Mapped[str]
    Cantidad2024: Mapped[int]
    CostoTotal2024: Mapped[int]
    Cantidad2025: Mapped[int]
    CostoTotal2025: Mapped[int]
    DiferenciaAnual: Mapped[int]
    DiferenciaDeCostos: Mapped[int] = mapped_column(nullable=True)
