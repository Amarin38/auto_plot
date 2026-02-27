from sqlalchemy.orm import Mapped
from infrastructure import DBBase
from infrastructure.db.models.base_model_mixin import BaseModelMixin


class MaximosMinimosModel(DBBase, BaseModelMixin):
    __tablename__ = "MAXIMOS_MINIMOS"
    
    Familia:    Mapped[int]
    Articulo:   Mapped[int]
    Repuesto:   Mapped[str]
    Minimo:     Mapped[float]
    Maximo:     Mapped[float]