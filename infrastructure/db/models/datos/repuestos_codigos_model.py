from sqlalchemy import String
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from infrastructure import dbbase_sqlite


class RepuestosCodigosModel(dbbase_sqlite):
    __tablename__ = "data_repuestos_codigos"

    id:             Mapped[int] = mapped_column(primary_key=True)
    Descripcion:    Mapped[str]
    Deposito:       Mapped[str] = mapped_column(String(10))
    Familia:        Mapped[int]
    Articulo:       Mapped[int]
    Codigos:        Mapped[str] = mapped_column(String(10))
    CodigosConCero: Mapped[str] = mapped_column(String(10))