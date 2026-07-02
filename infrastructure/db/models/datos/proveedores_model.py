from sqlalchemy import String
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from infrastructure import DBBase


class ProveedoresModel(DBBase):
    __tablename__ = "PROVEEDORES"

    NroProv         : Mapped[int] = mapped_column(primary_key=True)
    RazonSocial     : Mapped[str]
    CUIT            : Mapped[str] = mapped_column(String(13), nullable=True)
    Localidad       : Mapped[str] = mapped_column(nullable=True)
    Mail            : Mapped[str] = mapped_column(nullable=True)
    Telefono        : Mapped[str] = mapped_column(String(10), nullable=True)