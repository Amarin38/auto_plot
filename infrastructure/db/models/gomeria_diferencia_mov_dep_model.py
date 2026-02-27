from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from infrastructure import DBBase
from infrastructure.db.models.base_model_mixin import BaseModelMixin


class GomeriaDiferenciaMovEntreDepModel(BaseModelMixin, DBBase):
    __tablename__ = "GOMERIA_DIFERENCIA_MOV_DEP"

    Familia: Mapped[int]
    Articulo: Mapped[int]
    Repuesto: Mapped[str]
    Cantidad2024: Mapped[int]
    CostoTotal2024: Mapped[int]
    Cantidad2025: Mapped[int]
    CostoTotal2025: Mapped[int]
    DiferenciaAnual: Mapped[int]
    DiferenciaDeCostos: Mapped[int] = mapped_column(nullable=True)
