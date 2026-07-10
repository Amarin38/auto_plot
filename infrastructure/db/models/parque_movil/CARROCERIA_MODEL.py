from sqlalchemy import String
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from infrastructure import dbbase_postgres


class CarroceriaModel(dbbase_postgres):
    __tablename__ = "CARROCERIA"

    IDCarroceria:      Mapped[int]         = mapped_column(primary_key=True)
    Marca:             Mapped[str]         = mapped_column(String(30), nullable=False)
