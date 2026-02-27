from datetime import date

from sqlalchemy import Date
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

from infrastructure import DBBase
from infrastructure.db.models.base_model_mixin import BaseModelMixin, BaseCabecera


class ConsumoObligatorioModel(BaseModelMixin, BaseCabecera, DBBase):
    __tablename__ = "CONSUMO_OBLIGATORIO"

    Repuesto:           Mapped[str]
    Año2023:            Mapped[int]
    Año2024:            Mapped[int]
    Año2025:            Mapped[int]
    MinimoAntiguo:      Mapped[int]
    MinimoObligatorio:  Mapped[int]
    UltimaFecha:        Mapped[date] = mapped_column(Date)