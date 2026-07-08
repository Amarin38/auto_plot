from sqlalchemy import String
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from infrastructure import dbbase_sqlite

class CochesCabeceraModel(dbbase_sqlite):
    __tablename__ = "data_coches_cabecera"

    id:                 Mapped[int] = mapped_column(primary_key=True)
    Cabecera:           Mapped[str] = mapped_column(String(40), index=True) #TODO: hacer index=true en los que hago groupby
    CochesDuermen:      Mapped[int] = mapped_column(nullable=True)
    CochesDuermenNuevo: Mapped[int] = mapped_column(nullable=True)
    CochesSinScania:    Mapped[int] = mapped_column(nullable=True)