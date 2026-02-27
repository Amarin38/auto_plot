from typing import Dict, Any
from sqlalchemy import JSON
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from infrastructure import DBBase
from infrastructure.db.models.base_model_mixin import BaseModelMixin


class JSONConfigModel(BaseModelMixin, DBBase):
    __tablename__ = "JSON_CONFIG"
    
    nombre:     Mapped[str]
    data:       Mapped[Dict[str, Any]] = mapped_column(JSON)









