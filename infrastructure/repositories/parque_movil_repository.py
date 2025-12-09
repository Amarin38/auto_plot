from datetime import date
from typing import List

import streamlit as st
from sqlalchemy import select, and_

from domain.entities.parque_movil import ParqueMovil
from infrastructure import SessionDB, db_engine
from infrastructure.db.models.parque_movil_model import ParqueMovilModel
from infrastructure.mappers.parque_movil_mapper import ParqueMovilMapper
from interfaces.repository import Repository


class ParqueMovilRepository(Repository):
        def __init__(self):
            self.session = SessionDB()
            self.engine = db_engine

        # Create -------------------------------------------
        def insert_many(self, entities: List[ParqueMovil]) -> None:
            with self.session as session:
                for e in entities:
                    model = ParqueMovilMapper.to_model(e)
                    session.add(model)
                    session.commit()

        # Read -------------------------------------------
        def get_all(self) -> List[ParqueMovil]:
            with self.session as session:
                models = session.scalars(
                    select(ParqueMovilModel)
                ).all()

                return [ParqueMovilMapper.to_entity(m) for m in models]

        def get_by_id(self, _id: int) -> ParqueMovil:
            with self.session as session:
                model = session.scalars(
                    select(ParqueMovilModel)
                ).filter(
                    ParqueMovilModel.id == _id
                ).first()

                return ParqueMovilMapper.to_entity(model)

        @staticmethod
        @st.cache_data
        def get_by_args(fecha_inicio: date, fecha_fin: date) -> List[ParqueMovil]:
            with SessionDB() as session:
                models = session.scalars(
                    select(ParqueMovilModel)
                    .where(ParqueMovilModel.FechaParqueMovil.between(fecha_inicio, fecha_fin))
                ).all()

                return [ParqueMovilMapper.to_entity(m) for m in models]

        # Delete -------------------------------------------
        def delete_by_id(self, _id: int) -> None:
            with self.session as session:
                with session.begin():
                    row = session.get(ParqueMovilModel, _id)
                    if row:
                        session.delete(row)