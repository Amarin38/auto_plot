from typing import List
from sqlalchemy.orm import Session
from sqlalchemy import select, delete

from domain.entities.datos_proveedores import Proveedores
from infrastructure.db.models.datos_proveedores_model import ProveedoresModel
from infrastructure.mappers.datos_proveedores_mapper import ProveedoresMapper
from interfaces.repository import Repository


class ProveedoresRepository(Repository):
    def __init__(self, session: Session):
        self.session = session

    # Create -------------------------------------------
    def insert_many(self, entities: List[Proveedores]) -> None:
        self.delete_all()
        models = [ProveedoresMapper.to_model(e) for e in entities]
        self.session.add_all(models)


    # Read -------------------------------------------
    def get_all(self) -> List[Proveedores]:
        models = self.session.scalars(
            select(ProveedoresModel)
        ).all()

        return [ProveedoresMapper.to_entity(m) for m in models]


    def get_by_id(self, nro_prov: int) -> Proveedores:
        model = self.session.scalars(
            select(ProveedoresModel).where(ProveedoresModel.NroProv == nro_prov)
        ).first()

        return ProveedoresMapper.to_entity(model)

    # Update -------------------------------------------
    def update(self, entity: Proveedores) -> None:
        model = self.session.get(ProveedoresModel, entity.NroProv)

        if model:
            model.RazonSocial = entity.RazonSocial
            model.CUIT        = entity.CUIT
            model.Localidad   = entity.Localidad
            model.Mail        = entity.Mail
            model.Telefono    = entity.Telefono


    def insert_one(self, entity: Proveedores) -> None:
        model = ProveedoresMapper.to_model(entity)
        self.session.add(model)


    # Delete -------------------------------------------
    def delete_by_id(self, nro_prov: int) -> None:
        row = self.session.get(ProveedoresModel, nro_prov)
        if row:
            self.session.delete(row)

    def delete_all(self) -> None:
        self.session.execute(delete(ProveedoresModel))
        self.session.commit()
