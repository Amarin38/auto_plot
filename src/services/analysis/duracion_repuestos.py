import pandas as pd

from src.utils.exception_utils import execute_safely


@execute_safely
def calcular_duracion(df: pd.DataFrame, repuesto_rep: str, tipo_duracion: str):
    patentes = df["Patente"].unique()

    for patente in patentes:
        df_separado = df["Patente"] == patente
        # separo por cada patende y traigo la columna Cambio, y a esa columna en ese espacio
        # le aplico el rango del tamaño de ese sub-dataframe
        df.loc[df_separado, "Cambio"] = range(len(df.loc[df_separado]))
        # TODO: queda calcular la duracion por dias

        df.loc[df_separado, "DuracionEnDias"] = df["FechaCambio"] - df["FechaCambio"].shift(1)

    df["Cambio"] = df["Cambio"].astype(int)
    df["DuracionEnDias"] = df["DuracionEnDias"].astype(int)
    df["DuracionEnMeses"] = round(df["DuracionEnDias"] / 30, 1)
    df["DuracionEnAños"] = round(df["DuracionEnDias"] / 365, 1)

    print(df)


