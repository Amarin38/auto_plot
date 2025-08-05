from typing import Dict
import pandas as pd
import json

# --- Actualizar consumo de gomeria --- #
def calcular_consumo_por_mes_gomeria(archivo: str) -> None:
    df: pd.DataFrame = pd.read_excel(f"{archivo}.xlsx",engine="calamine")
    
    with open("json/meses.json", "r") as m:
        meses: Dict[str,int] = json.load(m)

    consumo_cantidad: Dict[str,int] = {}
    consumo_plata: Dict[str,int] = {}
    
    for mes, num_mes in meses.items():
        df_filtrado = df[df["FechaCompleta"].dt.month == num_mes] # separo por mes

        cantidad_total_por_mes = df.iloc[df_filtrado.index, 11].sum() # sumo consumo en ese mes
        precio_total_por_mes = (df.iloc[df_filtrado.index, 11] * df.iloc[df_filtrado.index, 13]).sum() # sumo el consumo en plata en ese mes 

        consumo_cantidad.update({f"{mes}":int(cantidad_total_por_mes)}) # agrego a sus respectivos diccionarios
        consumo_plata.update({f"{mes}":round(float(precio_total_por_mes),2)}) # type: ignore
    
    with open(f"json/cubiertas-consumo-{archivo}.json", "w") as file:
        json.dump({"cantidad":[consumo_cantidad],
                   "plata":[consumo_plata]}, file, indent=4)
    

def actualizar_valores_cubiertas(archivo: str) -> Dict[str, float]:
    meses: list[str] = ["enero", "febrero", "marzo", "abril", "mayo", "junio"]
    indice_consumo_por_mes: Dict[str, float] = {}

    with open("json/cubiertas-armadas.json", "r") as f1:
        data_armadas = json.load(f1)
    
    with open(f"json/{archivo}.json", "r") as f2:
        data_consumo = json.load(f2)
    
    for m in meses:
        total_consumo = round(data_consumo["plata"][0][m]/data_armadas["cantidad"][0][m], 2) 
        indice_consumo_por_mes.update({m:total_consumo})

    
    return indice_consumo_por_mes
