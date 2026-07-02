from typing import List

from sqlalchemy import select
from sqlalchemy.orm import Session

from config.enums import PeriodoComparacionEnum, ConsumoComparacionRepuestoEnum, CabecerasEnum
from domain.entities.consumo.comparacion import ConsumoComparacion
from infrastructure.db.models.consumo.comparacion_model import ConsumoComparacionModel
from infrastructure.mapper import Mapper


class ConsumoComparacionRepository:
    def __init__(self, session: Session):
        self.session = session

    # Create -------------------------------------------
    def insert_many(self, entities: List[ConsumoComparacion]) -> None:
        models = [Mapper.to_model(entity, ConsumoComparacionModel) for entity in entities]
        self.session.add_all(models)


    # Read -------------------------------------------
    def get_all(self) -> List[ConsumoComparacion]:
        models = self.session.scalars(
            select(ConsumoComparacionModel)
        ).all()

        return [Mapper.to_entity(model, ConsumoComparacion) for model in models]


    def get_by_id(self, _id: int) -> ConsumoComparacion:
        model = self.session.scalars(
            select(ConsumoComparacionModel).where(ConsumoComparacionModel.id == _id)
        ).first()

        return Mapper.to_entity(model, ConsumoComparacion)


    def get_by_cabecera_and_tipo_rep_and_periodo(self, cabecera: CabecerasEnum,
                                                 tipo_repuesto: List[ConsumoComparacionRepuestoEnum],
                                                 periodo: List[PeriodoComparacionEnum]) -> List[ConsumoComparacion]:
        models = self.session.scalars(
            select(ConsumoComparacionModel)
            .where(ConsumoComparacionModel.Cabecera == cabecera,
                    ConsumoComparacionModel.TipoRepuesto.in_(tipo_repuesto),
                    ConsumoComparacionModel.PeriodoID.in_(periodo),
                   )
        )

        return [Mapper.to_entity(model, ConsumoComparacion) for model in models]

    # Delete -------------------------------------------
    def delete_by_id(self, _id: int) -> None:
        row = self.session.get(ConsumoComparacionModel, _id)
        if row:
            self.session.delete(row)
