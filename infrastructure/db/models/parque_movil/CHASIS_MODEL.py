from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from infrastructure import dbbase_postrgres


class ChasisModel(dbbase_postrgres):
    __tablename__ = "CHASIS"

    IDChasis:           Mapped[int]     = mapped_column(primary_key=True)
    IDChasisModelo:     Mapped[int]     = mapped_column(ForeignKey("CHASIS_MODELO.IDChasisModelo"))
    ChasisCodigo:       Mapped[str]     = mapped_column(String(50), unique=True)
