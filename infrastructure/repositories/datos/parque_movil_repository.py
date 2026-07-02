from datetime import date
from typing import List

import streamlit as st
from sqlalchemy import select
from sqlalchemy.orm import Session

from domain.entities.datos.parque_movil import ParqueMovil
from infrastructure.db.models.datos.parque_movil_model import ParqueMovilModel
from infrastructure.mapper import Mapper


class ParqueMovilRepository:
        def __init__(self, session: Session):
            self.session = session

        # Create -------------------------------------------
        def insert_many(self, entities: List[ParqueMovil]) -> None:
            models = [Mapper.to_model(entity, ParqueMovilModel) for entity in entities]
            self.session.add_all(models)


        # Read -------------------------------------------
        def get_all(self) -> List[ParqueMovil]:
            models = self.session.scalars(
                select(ParqueMovilModel)
            ).all()

            return [Mapper.to_entity(model, ParqueMovil) for model in models]


        def get_by_id(self, _id: int) -> ParqueMovil:
            model = self.session.scalars(
                select(ParqueMovilModel).where(ParqueMovilModel.id == _id)
            ).first()

            return Mapper.to_entity(model, ParqueMovil)


        @st.cache_data
        def get_by_args(_self, fecha_inicio: date, fecha_fin: date) -> List[ParqueMovil]:
            models = _self.session.scalars(
                select(ParqueMovilModel)
                .where(ParqueMovilModel.FechaParqueMovil.between(fecha_inicio, fecha_fin))
            ).all()

            return [Mapper.to_entity(model, ParqueMovil) for model in models]


        # Delete -------------------------------------------
        def delete_by_id(self, _id: int) -> None:
            row = self.session.get(ParqueMovilModel, _id)
            if row:
                self.session.delete(row)