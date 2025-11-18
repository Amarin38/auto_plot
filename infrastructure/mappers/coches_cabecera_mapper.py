from domain.entities.coches_cabecera import CochesCabecera
from infrastructure.db.models.coches_cabecera_model import CochesCabeceraModel
from interfaces.mapper import Mapper


class CochesCabeceraMapper(Mapper):
    @staticmethod
    def to_entity(model: CochesCabeceraModel) -> CochesCabecera:
        return CochesCabecera(
            id                  = model.id,
            Cabecera            = model.Cabecera,
            CochesDuermen       = model.CochesDuermen,
            CochesDuermenNuevo  = model.CochesDuermenNuevo,
            CochesSinScania     = model.CochesSinScania,
        )

    @staticmethod
    def to_model(entity: CochesCabecera) -> CochesCabeceraModel:
        return CochesCabeceraModel(
            id                  = entity.id,
            Cabecera            = entity.Cabecera,
            CochesDuermen       = entity.CochesDuermen,
            CochesDuermenNuevo  = entity.CochesDuermenNuevo,
            CochesSinScania     = entity.CochesSinScania,
        )