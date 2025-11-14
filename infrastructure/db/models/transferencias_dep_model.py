from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from infrastructure import DBBase


class TransferenciasEntreDepositosModel(DBBase):
    __tablename__ = "TRANSFERENCIAS_DEP"

    id: Mapped[int] = mapped_column(primary_key=True)
    Repuesto: Mapped[str]
    Año: Mapped[int]
    Cantidad: Mapped[int]
    Cabecera: Mapped[str]
