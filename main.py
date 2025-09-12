import os, sys, json
import pandas as pd

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
from src.services.data_cleaning.inventory_data_cleaner import InventoryDataCleaner
from src.db import Base, engine
from src.db.models.json_config_model import JSONConfig
from src.db.crud import json_to_sql, store_json_file, read_json_config

# from src.db.models.coches_cabecera_model import CochesCabecera
# from src.db.models.internos_cabecera_model import InternosCabecera
# from src.db.models.motores_cabecera_model import MotoresCabecera
# from src.db.models.forecast_data_model import ForecastData
# from src.db.models.forecast_trend_model import ForecastTrend
# from src.db.models.index_repuesto_model import IndexRepuesto
# from src.db.models.internos_asignados_model import InternosAsignados
# from src.db.models.maxmin_model import Maxmin


if __name__ == "__main__":
    Base.metadata.create_all(engine)
    # store_json_file("nombres_inyectores")
    

    ...



