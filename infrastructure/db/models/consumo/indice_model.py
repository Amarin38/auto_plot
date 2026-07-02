from datetime import date
from decimal import Decimal
from sqlalchemy import Date, String, DECIMAL
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from infrastructure import DBBase


class ConsumoIndiceModel(DBBase):
    __tablename__ = "CONSUMO_INDICE"

    id:             Mapped[int] = mapped_column(primary_key=True)
    Cabecera:       Mapped[str] = mapped_column(String(40), index=True) #TODO: hacer index=true en los que hago groupby
    Repuesto:       Mapped[str] = mapped_column(String(150), index=True)
    TipoRepuesto:   Mapped[str]
    TotalConsumo:   Mapped[Decimal] = mapped_column(DECIMAL(10,2))
    TotalCoste:     Mapped[Decimal] = mapped_column(DECIMAL(10,2))
    IndiceConsumo:  Mapped[Decimal] = mapped_column(DECIMAL(10,2))
    UltimaFecha:    Mapped[date] = mapped_column(Date)
    TipoOperacion:  Mapped[str] = mapped_column(String(7))
    


