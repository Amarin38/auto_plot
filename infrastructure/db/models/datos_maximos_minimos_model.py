from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column
from infrastructure import DBBase
from infrastructure.db.models.base_model_mixin import BaseModelMixin


class MaximosMinimosModel(BaseModelMixin, DBBase):
    __tablename__ = "MAXIMOS_MINIMOS"
    
    Familia:    Mapped[int]
    Articulo:   Mapped[int]
    Repuesto:   Mapped[str] = mapped_column(String(150), index=True)
    Minimo:     Mapped[float]
    Maximo:     Mapped[float]