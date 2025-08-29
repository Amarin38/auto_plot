# from services.analysis.maxmin import MaxMin, MaxMinUtils
from services import IndexByVehicle
from services import InventoryDataCleaner, InventoryUpdate
# from services import FleetDataCleaner
# from services import ForecastWithZero, ForecastWithoutZero
from services import ScrapCodigosLicitaciones, ScrapMaxMin

if __name__ == "__main__":
    # maxmin = MaxMin("maxmin", fecha="19/08/2025")
    # maxmin.run_all()

    # maxmin_utils = MaxMinUtils("19/08/2025", web=True)
    # maxmin_utils.create_code_list(excel=True)    
    
    # indice = IndexByVehicle("", "todos flotantes gasoil")
    # indice.calculate_index()

    # scrap = ScrapCodigosLicitaciones("Sensor").scrap_to_df()
    # InventoryDataCleaner("fispa", "carp").run_all()

    InventoryUpdate("bombas_urea")._update_single_row_name(column="Repuesto", old_name="BOMBA DOSIFICADORA UREA EURO V REP.", new_name="BOMBA DOSIFICADORA UREA EURO V").reset_index() #type: ignore
    InventoryUpdate("bombas_urea")._update_single_row_name(column="Repuesto", old_name="BOMBA DOSIFICADORA UREA EURO V NVA", new_name="BOMBA DOSIFICADORA UREA EURO V").reset_index() #type: ignore

    # TODO: Aplicar el wrapper de execute_safely a todas las funciones
    ...


