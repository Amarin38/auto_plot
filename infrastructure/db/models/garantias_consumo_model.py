from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from infrastructure import DBBase
from infrastructure.db.models.base_model_mixin import BaseModelMixin


class GarantiasConsumoModel(DBBase, BaseModelMixin):
    __tablename__ = "GARANTIAS_CONSUMO"
    
    Cabecera:                   Mapped[str]
    Repuesto:                   Mapped[str]
    TipoRepuesto:               Mapped[str] = mapped_column(nullable=True)
    Garantia:                   Mapped[int]
    Transferencia:              Mapped[int]
    Total:                      Mapped[int]
    PorcentajeTransferencia:    Mapped[str]
    PorcentajeGarantia:         Mapped[str]
