from sqlalchemy import JSON
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from .. import Base

class JSONConfig(Base):
    __tablename__ = "json_config"
    
    id:         Mapped[int] = mapped_column(primary_key=True)
    nombre:     Mapped[str]
    data:       Mapped[JSON]









