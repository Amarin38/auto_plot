from pydantic import BaseModel, ConfigDict


class MaximosMinimos(BaseModel):
    Familia         : str
    Articulo        : str
    Descripcion     : str

    model_config = ConfigDict(from_attributes=True)

class MaximosMinimosStock(BaseModel):
    FamiliaStock        : str
    ArticuloStock       : str
    DescripcionStock    : str

    model_config = ConfigDict(from_attributes=True)

