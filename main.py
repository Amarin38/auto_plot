import os, sys, json
import pandas as pd

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
from src.services.data_cleaning.inventory_data_cleaner import InventoryDataCleaner
from src.db_data import Base, engine
from src.db_data.models.json_config_model import JSONConfigModel
from src.db_data.crud_services import json_to_sql, store_json_file, read_json_config

# from src.db.models.coches_cabecera_model import CochesCabeceraModel
# from src.db.models.internos_cabecera_model import InternosCabeceraModel
# from src.db.models.motores_cabecera_model import MotoresCabeceraModel
# from src.db.models.forecast_data_model import ForecastDataModel
# from src.db.models.forecast_trend_model import ForecastTrendModel
# from src.db.models.index_repuesto_model import IndexRepuestoModel
# from src.db.models.internos_asignados_model import InternosAsignadosModel
# from src.db.models.maxmin_model import MaxminModel


if __name__ == "__main__":
    Base.metadata.create_all(engine)
    # store_json_file("nombres_inyectores")
    

    ...



