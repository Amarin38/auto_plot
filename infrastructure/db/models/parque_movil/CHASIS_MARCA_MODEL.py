from sqlalchemy import String
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from infrastructure import DBBase


class ChasisMarcaModel(DBBase):
    __tablename__ = "CHASIS_MARCA"

    IDChasisMarca:    Mapped[int]     = mapped_column(primary_key=True)
    Nombre:           Mapped[str]     = mapped_column(String(50), nullable=False, unique=True)

