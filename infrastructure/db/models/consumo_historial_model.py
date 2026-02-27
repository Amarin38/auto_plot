from datetime import date

from sqlalchemy import Date
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from infrastructure import DBBase
from infrastructure.db.models.base_model_mixin import BaseModelMixin


class ConsumoHistorialModel(DBBase, BaseModelMixin):
    __tablename__ = "CONSUMO_HISTORIAL"

    TipoRepuesto:   Mapped[str]
    Año:            Mapped[int]
    TotalConsumo:   Mapped[float]
    FechaMin:       Mapped[date] = mapped_column(Date)
    FechaMax:       Mapped[date] = mapped_column(Date)

