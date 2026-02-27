from datetime import date
from sqlalchemy import Date, String
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from infrastructure import DBBase
from infrastructure.db.models.base_model_mixin import BaseModelMixin


class ConsumoPrevisionDataModel(BaseModelMixin, DBBase):
    __tablename__ = "CONSUMO_PREVISION_DATA"
    
    FechaCompleta:      Mapped[date] = mapped_column(Date)
    Consumo:            Mapped[int]
    Repuesto:           Mapped[str] = mapped_column(String(150), index=True)
    TipoRepuesto:       Mapped[str]
