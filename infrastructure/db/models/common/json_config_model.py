from typing import Dict, Any
from sqlalchemy import JSON
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from infrastructure import DBBase


class JSONConfigModel(DBBase):
    __tablename__ = "JSON_CONFIG"
    
    id:         Mapped[int] = mapped_column(primary_key=True)
    nombre:     Mapped[str]
    data:       Mapped[Dict[str, Any]] = mapped_column(JSON)









