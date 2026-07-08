from sqlalchemy import String
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from infrastructure import dbbase_sqlite


class GarantiasConsumoModel(dbbase_sqlite):
    __tablename__ = "stats_garantias_consumo"

    id:                         Mapped[int] = mapped_column(primary_key=True)
    Cabecera:                   Mapped[str] = mapped_column(String(40), index=True) #TODO: hacer index=true en los que hago groupby
    Repuesto:                   Mapped[str] = mapped_column(String(150), index=True)
    TipoRepuesto:               Mapped[str] = mapped_column(nullable=True)
    Garantia:                   Mapped[int]
    Transferencia:              Mapped[int]
    Total:                      Mapped[int]
    PorcentajeTransferencia:    Mapped[str]
    PorcentajeGarantia:         Mapped[str]
