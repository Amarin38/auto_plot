from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from infrastructure import DBBase
from infrastructure.db.models.base_model_mixin import BaseModelMixin


class CochesCabeceraModel(DBBase, BaseModelMixin):
    __tablename__ = "COCHES_CABECERA"
    
    Cabecera:           Mapped[str]
    CochesDuermen:      Mapped[int] = mapped_column(nullable=True)
    CochesDuermenNuevo: Mapped[int] = mapped_column(nullable=True)
    CochesSinScania:    Mapped[int] = mapped_column(nullable=True)