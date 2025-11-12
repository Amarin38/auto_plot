from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from infrastructure import ServicesBase


class TransferenciasEntreDepositosModel(ServicesBase):
    __tablename__ = "transferencias_entre_depositos"

    id: Mapped[int] = mapped_column(primary_key=True)
    Repuesto: Mapped[str]
    Año: Mapped[int]
    Cantidad: Mapped[int]
    Cabecera: Mapped[str]
