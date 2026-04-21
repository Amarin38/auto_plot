from domain.entities.datos_proveedores import Proveedores
from infrastructure.db.models.datos_proveedores_model import ProveedoresModel


class ProveedoresMapper:
    @staticmethod
    def to_entity(model: ProveedoresModel) -> Proveedores:
        return Proveedores(
            NroProv         = model.NroProv,
            RazonSocial     = model.RazonSocial,
            CUIT            = model.CUIT,
            Localidad       = model.Localidad,
            Mail            = model.Mail,
            Telefono        = model.Telefono
        )

    @staticmethod
    def to_model(entity: Proveedores) -> ProveedoresModel:
        return ProveedoresModel(
            NroProv         = entity.NroProv,
            RazonSocial     = entity.RazonSocial,
            CUIT            = entity.CUIT,
            Localidad       = entity.Localidad,
            Mail            = entity.Mail,
            Telefono        = entity.Telefono
        )