from sqlalchemy.orm import Mapped
from infrastructure import DBBase
from infrastructure.db.models.base_model_mixin import BaseModelMixin


class MaximosMinimosModel(BaseModelMixin, DBBase):
    __tablename__ = "MAXIMOS_MINIMOS"
    
    Familia:    Mapped[int]
    Articulo:   Mapped[int]
    Repuesto:   Mapped[str]
    Minimo:     Mapped[float]
    Maximo:     Mapped[float]