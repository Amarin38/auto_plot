from pydantic import BaseModel, ConfigDict


class Proveedores(BaseModel):
    NroProv         : int
    RazonSocial     : str
    CUIT            : str
    Localidad       : str
    Mail            : str
    Telefono        : str

    model_config = ConfigDict(from_attributes=True)