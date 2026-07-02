from sqlalchemy import String
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from infrastructure import DBBase


class CarroceriaModel(DBBase):
    __tablename__ = "CARROCERIA"

    IDCarroceria:      Mapped[int]         = mapped_column(primary_key=True)
    Marca:             Mapped[str]         = mapped_column(String(30), nullable=False)
