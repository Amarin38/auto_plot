import os, sys
import pandas as pd


sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
from src.services.data_cleaning.inventory_data_cleaner import InventoryDataCleaner

# from src.db.crud import df_to_sql, sql_to_df

# from src.db import Base, engine
# from src.db.models.coches_cabecera_model import CochesCabecera
# from src.db.models.internos_cabecera_model import InternosCabecera
# from src.db.models.motores_cabecera_model import MotoresCabecera
# from src.db.models.forecast_data_model import ForecastData
# from src.db.models.forecast_trend_model import ForecastTrend
# from src.db.models.index_repuesto_model import IndexRepuesto
# from src.db.models.internos_asignados_model import InternosAsignados
# from src.db.models.maxmin_model import Maxmin

from src.config.constants import JSON_PATH

if __name__ == "__main__":
    # Base.metadata.create_all(engine)
    df = pd.read_json(f"{JSON_PATH}/columns.json", lines=True) 
    print(df)
    # print(sql_to_df("motores_cabecera"))
    # df = pd.read_excel(f"{EXCEL_PATH}/internos_asignados_cabecera.xlsx")
    # df = pd.read_excel(f"{EXCEL_PATH}/internos_por_cabecera.xlsx")
    # df = pd.read_excel(f"{EXCEL_PATH}/motores_por_cabecera.xlsx")


    # df_to_sql("internos_asignados", df, "append")
    # delete = InventoryDataCleaner("inyectores-S").filter_repuesto("INYECTOR", "startswith")
    # a = InventoryDataCleaner().run_all("todo")

    # print(a)
    # df = pd.read_excel(f"{OUT_PATH}/inyectores_indice_por_coche.xlsx")
    # df_to_sql("indice_repuesto", df)
    
    # for indice in read_all("indice_repuesto"):
    #     print(indice)


    # maxmin = MaxMin("maxmin", "todo maxmin", "02/09/2025").calculate()
    ...



