import datetime
from typing import List

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

        def get_by_args(self, fecha_inicio: datetime.date, fecha_fin: datetime.date,
                              linea: int, interno: int, dominio: str, chasis_modelos: List[str]) -> List[ParqueMovil]:
            filtros = []

            with self.session as session:
                if fecha_inicio and fecha_fin:
                    filtros.append(ParqueMovilModel.FechaParqueMovil.between(fecha_inicio, fecha_fin))

                if linea:
                    filtros.append(ParqueMovilModel.Linea == linea)

                if interno:
                    filtros.append(ParqueMovilModel.Interno == interno)

                if dominio:
                    filtros.append(ParqueMovilModel.Dominio.like("%"+dominio+"%"))

                if chasis_modelos:
                    filtros.append(ParqueMovilModel.ChasisModelo.in_(chasis_modelos))

                stmt = select(ParqueMovilModel)

                if filtros:
                    stmt = session.scalars(
                        stmt.where(and_(*filtros))
                    ).all()

                return [ParqueMovilMapper.to_entity(m) for m in stmt]

        # Delete -------------------------------------------
        def delete_by_id(self, _id: int) -> None:
            with self.session as session:
                with session.begin():
                    row = session.get(ParqueMovilModel, _id)
                    if row:
                        session.delete(row)