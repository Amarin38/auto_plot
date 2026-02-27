from sqlalchemy.orm import Mapped, mapped_column


class BaseModelMixin:
    id : Mapped[int] = mapped_column(primary_key=True)
