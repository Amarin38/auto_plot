from datetime import date
from decimal import Decimal
from sqlalchemy import ForeignKey, Date, DECIMAL
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from infrastructure import dbbase_postgres


class RegistroKMModel(dbbase_postgres):
    __tablename__ = "REGISTRO_KM"

    IDRegistroKM:       Mapped[int]         = mapped_column(primary_key=True)
    IDParqueMovil:      Mapped[int]         = mapped_column(ForeignKey("PARQUE_MOVIL.IDParqueMovil"))
    FechaLectura:       Mapped[date]        = mapped_column(Date, nullable=False)
    KMTotal:            Mapped[Decimal]     = mapped_column(DECIMAL(10, 2), nullable=False)
