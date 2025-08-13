from plot_backend import MaxMin, ArreglarListadoExistencias, UtilsMaxMin

def calc_maxmin():
    arreglar = ArreglarListadoExistencias("maxmin", "todo maxmin")
    arreglar.arreglar_listado()

    utils = UtilsMaxMin("12/08/2025", "a", True)
    arreglar = ArreglarListadoExistencias("maxmin-S")

    arreglar.filter("lista_codigos", utils.generar_lista_codigos(False))

    maxmin = MaxMin("lista", 2.5)
    maxmin.calcular()

if __name__ == "__main__":
    calc_maxmin()
    ...


