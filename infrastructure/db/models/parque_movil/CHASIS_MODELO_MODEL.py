from sqlalchemy import String, ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from infrastructure import dbbase_postrgres


class ChasisModeloModel(dbbase_postrgres):
    __tablename__ = "CHASIS_MODELO"

    IDChasisModelo:    Mapped[int]     = mapped_column(primary_key=True)
    IDChasisMarca:     Mapped[int]     = mapped_column(ForeignKey("CHASIS_MARCA.IDChasisMarca"))
    Nombre:            Mapped[str]     = mapped_column(String(50), nullable=False)

    __table_args__ = (UniqueConstraint("IDChasisMarca", "Nombre", name="unique_chasis_marca_modelo"),)