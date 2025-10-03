from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from ... import ServicesBase

class ConsumoGarantiasModel(ServicesBase):
    __tablename__ = "consumo_garantias"
    
    id:             Mapped[int] = mapped_column(primary_key=True)
    Cabecera:       Mapped[str]
    Garantia:       Mapped[int]
    Transferencia:  Mapped[int]
    Total:          Mapped[int]
