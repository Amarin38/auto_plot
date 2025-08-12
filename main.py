from plot_backend import MaxMin, ArreglarListadoExistencias, GeneralUtils, UtilsMaxMin



if __name__ == "__main__":
    # arreglar = ArreglarListadoExistencias("141 a 513-S", "todo maxmin")

    # arreglar.arreglar_listado()



    # utils = UtilsMaxMin("licitaciones1")
    # utils2 = UtilsMaxMin("licitaciones2")

    # print(utils2.generar_lista_codigos())


    # arreglar.filter("lista_codigos", utils2.generar_lista_codigos())

    # general = GeneralUtils("maxmin-S", "maxmin")
    # general.append_df(True)

    maxmin = MaxMin("maxmin-S", 2.5)
    maxmin.calcular()


    ...


