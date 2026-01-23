from domain.entities.conteo_stock import ConteoStock
from infrastructure.db.models.conteo_stock_model import ConteoStockModel


class ConteoStockMapper:
    @staticmethod
    def to_entity(model: ConteoStockModel) -> ConteoStock:
        return ConteoStock(
            id              = model.id,
            Codigo          = model.Codigo,
            Articulo        = model.Articulo,
            Sistema         = model.Sistema,
            Recuento        = model.Recuento,
            Resultado       = model.Resultado,
            Fecha           = model.Fecha,
            Reconteos       = model.Reconteos,
            Estanteria      = model.Estanteria,
            Precio          = model.Precio,
            DiferenciaStock = model.DiferenciaStock,
            DiferenciaPrecio= model.DiferenciaPrecio,
            PrecioAnterior  = model.PrecioAnterior,
            PrecioActual    = model.PrecioActual,
            Alerta          = model.Alerta,
            Deposito        = model.Deposito,
            Ajuste          = model.Ajuste,
            StockNuevo      = model.StockNuevo,
        )

    @staticmethod
    def to_model(entity: ConteoStock) -> ConteoStockModel:
        return ConteoStockModel(
            id              = entity.id,
            Codigo          = entity.Codigo,
            Articulo        = entity.Articulo,
            Sistema         = entity.Sistema,
            Recuento        = entity.Recuento,
            Resultado       = entity.Resultado,
            Fecha           = entity.Fecha,
            Reconteos       = entity.Reconteos,
            Estanteria      = entity.Estanteria,
            Precio          = entity.Precio,
            DiferenciaStock = entity.DiferenciaStock,
            DiferenciaPrecio= entity.DiferenciaPrecio,
            PrecioAnterior  = entity.PrecioAnterior,
            PrecioActual    = entity.PrecioActual,
            Alerta          = entity.Alerta,
            Deposito        = entity.Deposito,
            Ajuste          = entity.Ajuste,
            StockNuevo      = entity.StockNuevo,
        )