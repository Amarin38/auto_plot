from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column


class BaseModelMixin:
    id: Mapped[int] = mapped_column(primary_key=True)

class BaseCabecera:
    Cabecera: Mapped[str] = mapped_column(String(40), index=True)
