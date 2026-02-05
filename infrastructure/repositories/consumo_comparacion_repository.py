from typing import List

from sqlalchemy import select

from config.enums import PeriodoComparacionEnum, ConsumoComparacionRepuestoEnum, CabecerasEnum
from domain.entities.consumo_comparacion import ConsumoComparacion
from infrastructure import SessionDB, db_engine
from infrastructure.db.models.consumo_comparacion_model import ConsumoComparacionModel
from infrastructure.mappers.consumo_comparacion_mapper import ConsumoComparacionMapper
from interfaces.repository import Repository


class ConsumoComparacionRepository(Repository):
    def __init__(self):
        self.session = SessionDB()
        self.engine = db_engine

    # Create -------------------------------------------
    def insert_many(self, entities: List[ConsumoComparacion]) -> None:
        with self.session as session:
            for e in entities:
                model = ConsumoComparacionMapper.to_model(e)
                session.add(model)
                session.commit()


    # Read -------------------------------------------
    def get_all(self) -> List[ConsumoComparacion]:
        with self.session as session:
            models = session.scalars(
                select(ConsumoComparacionModel)
            ).all()

            return [ConsumoComparacionMapper.to_entity(m) for m in models]


    def get_by_id(self, _id: int) -> ConsumoComparacion:
        with self.session as session:
            model = session.scalars(
                select(ConsumoComparacionModel)
            ).filter(
                ConsumoComparacionModel.id == _id
            ).first()

            return ConsumoComparacionMapper.to_entity(model)


    def get_by_cabecera_and_tipo_rep_and_periodo(self, cabecera: CabecerasEnum,
                                                 tipo_repuesto: List[ConsumoComparacionRepuestoEnum],
                                                 periodo: List[PeriodoComparacionEnum]) -> List[ConsumoComparacion]:
        with self.session as session:
            model = session.scalars(
                select(ConsumoComparacionModel)
                .where(ConsumoComparacionModel.Cabecera == cabecera,
                        ConsumoComparacionModel.TipoRepuesto.in_(tipo_repuesto),
                        ConsumoComparacionModel.PeriodoID.in_(periodo),
                       )
            )

            return [ConsumoComparacionMapper.to_entity(m) for m in model]

    # Delete -------------------------------------------
    def delete_by_id(self, _id: int) -> None:
        with self.session as session:
            with session.begin():
                row = session.get(ConsumoComparacionModel, _id)
                if row:
                    session.delete(row)
