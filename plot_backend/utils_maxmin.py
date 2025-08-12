import re
import time
import datetime

import pandas as pd

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

from bs4 import BeautifulSoup
from typing import List

from constants import MAIN_PATH

# TODO arreglar el webscraper para que funcione mejor y sacar el codigo que no es necesario y ver de eliminar
# la funcion scrapear_licitaciones

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


    def obtener_html(self):
        try:
            driver = webdriver.Firefox()
        except:
            driver = webdriver.Chrome()
        
        driver.get("https://dota.sistemasanantonio.com.ar/licitaciones/login.aspx")
        
        email = driver.find_element(By.NAME, "inputEmail")
        email.send_keys("garantias")
        passwd = driver.find_element(By.NAME, "inputPassword")
        passwd.send_keys("DOTA2024")

        login = driver.find_element(By.ID, "btn_iniciar")
        login.click()
        time.sleep(2)

        licitaciones = driver.find_element(By.XPATH, "//a[@href='#']//div[@class='hover thumbnail']//div[@class='caption']")
        licitaciones.click()
        
        try:
            fecha_input = driver.find_element(By.NAME, "ctl00$MainContent$txt_fecha_desde")
        except NoSuchElementException:
            fecha_input = driver.find_element(By.ID, "MainContent_txt_fecha_desde")

        fecha_input.clear()
        fecha_input.send_keys(datetime.date.today().strftime("%d/%m/%Y"))
        time.sleep(1)

        buscar_boton = driver.find_element(By.ID, "MainContent_btn_buscar")
        buscar_boton.click()
        time.sleep(1)

        busqueda_input = driver.find_element(By.XPATH, "//input[@type='search']")
        busqueda_input.clear()
        busqueda_input.send_keys("Finalizada Ningún pedido realizado")
        time.sleep(1)

        numeros_licitaciones = driver.find_elements(By.CLASS_NAME, "sorting_1")
        
        lista_numeros_licitaciones: List[str] = [p.text for p in numeros_licitaciones]
        lista_final: List[List[str]] = []

        for numero in lista_numeros_licitaciones:
            driver.get(f"https://dota.sistemasanantonio.com.ar/licitaciones/licitacion_sel.aspx?id={numero}")

            cod = driver.find_element(By.XPATH, "//th[@aria-label='cod: Activar para ordenar la columna de manera ascendente']")
            cod.click()

            numero_lic = driver.find_elements(By.CLASS_NAME, "sorting_1")

            lista_aux = [num.text for num in numero_lic]
            lista_final.append(lista_aux)
        
        lista_resultado_final = []
        for lista in lista_final:
            lista_resultado_final += lista
        
        return lista_resultado_final
    


    def scrapear_licitaciones(self) -> List[str]:
        lista_codigos: list[str] = []

        with open(f"{MAIN_PATH}/extracted.html", "r") as txt:
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
    utils.obtener_html()
    # utils.generar_lista_codigos()