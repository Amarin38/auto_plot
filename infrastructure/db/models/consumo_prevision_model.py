from datetime import date
from sqlalchemy import Date
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from infrastructure import DBBase
from infrastructure.db.models.base_model_mixin import BaseModelMixin


class ConsumoPrevisionModel(DBBase, BaseModelMixin):
    __tablename__ = "CONSUMO_PREVISION"

    FechaCompleta:      Mapped[date] = mapped_column(Date)
    Prevision:          Mapped[int]
    Repuesto:           Mapped[str]
    TipoRepuesto:       Mapped[str]
