import os, sys
import pandas as pd


sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
from src.services.data_cleaning.inventory_data_cleaner import InventoryDataCleaner
from src.services.analysis.maxmin import MaxMin

if __name__ == "__main__":
    # delete = InventoryDataCleaner("inyectores-S").filter_repuesto("INYECTOR", "startswith")

    # df = pd.read_excel(f"{OUT_PATH}/inyectores_indice_por_coche.xlsx")
    # df_to_sql("indice_repuesto", df)
    
    # for indice in read_all("indice_repuesto"):
    #     print(indice)


    # maxmin = MaxMin("maxmin", "todo maxmin", "02/09/2025").calculate()
    ...



