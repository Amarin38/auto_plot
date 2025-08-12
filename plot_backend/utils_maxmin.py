import re

import pandas as pd

from bs4 import BeautifulSoup
from typing import List

from plot_backend.constants import MAIN_PATH

# TODO falta hacer el scraper de la web con selenium
# para poder usarlo es necesario tocar en filtrar para que le asigne un nombre a la clase en la pagina
# de ahi se agrega al html y despues se ejecuta.


class UtilsMaxMin:
    def __init__(self, archivo_html: str) -> None:
        self.archivo_html = archivo_html


    def generar_lista_codigos(self) -> List[str]:
        lista_aux = []
        lista_codigos = self.scrapear_licitaciones()

        for codigo in lista_codigos:
            lista_aux.append(self.limpiar_codigo(codigo))
        
        # df = pd.DataFrame({"Codigos":lista_aux})
        # df.to_excel(f"{self.archivo_html}.xlsx")

        return lista_aux


    def scrapear_licitaciones(self) -> List[str]:
        lista_codigos: list[str] = []

        with open(f"{MAIN_PATH}/{self.archivo_html}.html", "r") as txt:
            soup = BeautifulSoup(txt, 'lxml')
            td_list = list(soup.find_all(class_="sorting_1"))
            
            for td in td_list:
                eliminar_td = re.sub('</td>', "", td.get_text())
                eliminar_td = re.sub('<td class="sorting_1">', "", eliminar_td)
                lista_codigos.append(eliminar_td)
            
        return lista_codigos
    

    def limpiar_codigo(self, filtro: str) -> str:
        total_ceros = 5
        filtro_spliteado = filtro.split(".")
        diferencia_ceros = total_ceros-len(filtro_spliteado[1])
        
        return f"{filtro_spliteado[0]}.{"0"*diferencia_ceros}{filtro_spliteado[1]}"  



if __name__ == "__main__":
    utils = UtilsMaxMin("licitaciones1")
    utils.generar_lista_codigos()