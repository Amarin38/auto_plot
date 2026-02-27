from datetime import date
from sqlalchemy import Date, String
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from infrastructure import DBBase
from infrastructure.db.models.base_model_mixin import BaseModelMixin, BaseCabecera, BaseRepuesto


class ConsumoIndiceModel(BaseModelMixin, BaseCabecera, BaseRepuesto, DBBase):
    __tablename__ = "CONSUMO_INDICE"

    TipoRepuesto:  Mapped[str]
    TotalConsumo:  Mapped[float]
    TotalCoste:    Mapped[float]
    IndiceConsumo: Mapped[float]
    UltimaFecha:   Mapped[date] = mapped_column(Date)
    TipoOperacion: Mapped[str] = mapped_column(String(7))
    


