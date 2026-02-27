from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from infrastructure import DBBase
from infrastructure.db.models.base_model_mixin import BaseModelMixin, BaseCabecera


class CochesCabeceraModel(BaseModelMixin, BaseCabecera, DBBase):
    __tablename__ = "COCHES_CABECERA"
    
    CochesDuermen:      Mapped[int] = mapped_column(nullable=True)
    CochesDuermenNuevo: Mapped[int] = mapped_column(nullable=True)
    CochesSinScania:    Mapped[int] = mapped_column(nullable=True)