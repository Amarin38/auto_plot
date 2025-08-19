from services import MaxMin
from services import RateByVehicle
from services import FleetDataCleaner
# from services import ForecastWithZero, ForecastWithoutZero


if __name__ == "__main__":
    # maxmin = MaxMin("maxmin", fecha="15/08/2025")
    # maxmin.run_all()
    
    flota = FleetDataCleaner("flota7")
    flota.count_motors_by_cabecera()
    # indice = RateByVehicle("flotantes_gasoil", "todos flotantes gasoil")
    # indice.calcular()
    ...


