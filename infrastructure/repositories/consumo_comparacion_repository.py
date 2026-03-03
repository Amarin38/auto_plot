from typing import List

from sqlalchemy import select
from sqlalchemy.orm import Session

from config.enums import PeriodoComparacionEnum, ConsumoComparacionRepuestoEnum, CabecerasEnum
from domain.entities.consumo_comparacion import ConsumoComparacion
from infrastructure.db.models.consumo_comparacion_model import ConsumoComparacionModel
from infrastructure.mappers.consumo_comparacion_mapper import ConsumoComparacionMapper
from interfaces.repository import Repository


class ConsumoComparacionRepository(Repository):
    def __init__(self, session: Session):
        self.session = session

    # Create -------------------------------------------
    def insert_many(self, entities: List[ConsumoComparacion]) -> None:
        models = [ConsumoComparacionMapper.to_model(e) for e in entities]
        self.session.add_all(models)


    # Read -------------------------------------------
    def get_all(self) -> List[ConsumoComparacion]:
        models = self.session.scalars(
            select(ConsumoComparacionModel)
        ).all()

        return [ConsumoComparacionMapper.to_entity(m) for m in models]


    def get_by_id(self, _id: int) -> ConsumoComparacion:
        model = self.session.scalars(
            select(ConsumoComparacionModel).where(ConsumoComparacionModel.id == _id)
        ).first()

        return ConsumoComparacionMapper.to_entity(model)


    def get_by_cabecera_and_tipo_rep_and_periodo(self, cabecera: CabecerasEnum,
                                                 tipo_repuesto: List[ConsumoComparacionRepuestoEnum],
                                                 periodo: List[PeriodoComparacionEnum]) -> List[ConsumoComparacion]:
        model = self.session.scalars(
            select(ConsumoComparacionModel)
            .where(ConsumoComparacionModel.Cabecera == cabecera,
                    ConsumoComparacionModel.TipoRepuesto.in_(tipo_repuesto),
                    ConsumoComparacionModel.PeriodoID.in_(periodo),
                   )
        )

        return [ConsumoComparacionMapper.to_entity(m) for m in model]

    # Delete -------------------------------------------
    def delete_by_id(self, _id: int) -> None:
        row = self.session.get(ConsumoComparacionModel, _id)
        if row:
            self.session.delete(row)
