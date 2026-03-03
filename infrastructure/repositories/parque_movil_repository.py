from datetime import date
from typing import List

import streamlit as st
from sqlalchemy import select
from sqlalchemy.orm import Session

from domain.entities.parque_movil import ParqueMovil
from infrastructure.db.models.parque_movil_model import ParqueMovilModel
from infrastructure.mappers.parque_movil_mapper import ParqueMovilMapper
from interfaces.repository import Repository


class ParqueMovilRepository(Repository):
        def __init__(self, session: Session):
            self.session = session

        # Create -------------------------------------------
        def insert_many(self, entities: List[ParqueMovil]) -> None:
            models = [ParqueMovilMapper.to_model(e) for e in entities]
            self.session.add_all(models)


        # Read -------------------------------------------
        def get_all(self) -> List[ParqueMovil]:
            models = self.session.scalars(
                select(ParqueMovilModel)
            ).all()

            return [ParqueMovilMapper.to_entity(m) for m in models]


        def get_by_id(self, _id: int) -> ParqueMovil:
            model = self.session.scalars(
                select(ParqueMovilModel).where(ParqueMovilModel.id == _id)
            ).first()

            return ParqueMovilMapper.to_entity(model)


        @st.cache_data
        def get_by_args(_self, fecha_inicio: date, fecha_fin: date) -> List[ParqueMovil]:
            models = _self.session.scalars(
                select(ParqueMovilModel)
                .where(ParqueMovilModel.FechaParqueMovil.between(fecha_inicio, fecha_fin))
            ).all()

            return [ParqueMovilMapper.to_entity(m) for m in models]


        # Delete -------------------------------------------
        def delete_by_id(self, _id: int) -> None:
            row = self.session.get(ParqueMovilModel, _id)
            if row:
                self.session.delete(row)