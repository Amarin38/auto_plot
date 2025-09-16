import re
import pandas as pd

from bs4 import BeautifulSoup
from typing import List

from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

from src.config.constants import MAIN_PATH
from src.services.scrapping.scrap_utils import ScrapUtils 
from src.utils.exception_utils import execute_safely

class ScrapMaxMin:
    def __init__(self, fecha_desde: str) -> None:
        self.fecha_desde = fecha_desde
    
    @execute_safely
    def web(self) -> List[str]:
        lista_codigos: List[str] = []
        driver, wait = ScrapUtils().login_licitaciones() # type: ignore
        
        try:
            ScrapUtils.wait_by_name(wait, "ctl00$MainContent$txt_fecha_desde")
            fecha_input = driver.find_element(By.NAME, "ctl00$MainContent$txt_fecha_desde")
        except NoSuchElementException:
            ScrapUtils.wait_by_id(wait, "MainContent_txt_fecha_desde")
            fecha_input = driver.find_element(By.ID, "MainContent_txt_fecha_desde")

        fecha_input.clear()
        fecha_input.send_keys(self.fecha_desde)

        ScrapUtils.wait_by_id(wait, "MainContent_btn_buscar")
        buscar_boton = driver.find_element(By.ID, "MainContent_btn_buscar")
        buscar_boton.click()

        ScrapUtils.wait_by_xpath(wait, "//input[@type='search']")
        busqueda_input = driver.find_element(By.XPATH, "//input[@type='search']")
        busqueda_input.clear()
        busqueda_input.send_keys("Finalizada Ningún pedido realizado Pompeya")

        ScrapUtils.wait_by_class(wait, "sorting_1")
        codigos_licitaciones = driver.find_elements(By.CLASS_NAME, "sorting_1")
        lista_numeros_licitaciones: List[str] = [codigo.text for codigo in codigos_licitaciones]

        for numero in lista_numeros_licitaciones:
            driver.get(f"https://dota.sistemasanantonio.com.ar/licitaciones/licitacion_sel.aspx?id={numero}")

            ordenar_columna = driver.find_element(By.XPATH, "//th[@aria-label='cod: Activar para ordenar la columna de manera ascendente']")
            ordenar_columna.click()

            ScrapUtils.wait_by_class(wait, "sorting_1")
            codigo_repuesto = driver.find_elements(By.CLASS_NAME, "sorting_1")

            lista_codigos += [codigo.text for codigo in codigo_repuesto]
        driver.quit()

        return lista_codigos
    

    @execute_safely
    def web_to_excel(self) -> None:
        df = pd.DataFrame(self.web(), columns=["Codigos"])
        df.to_excel(f"{MAIN_PATH}/codigos_maxmin.xlsx")


    @execute_safely
    def local(self) -> List[str]:
        lista_codigos: list[str] = []

        with open(f"{MAIN_PATH}/extracted.html", "r") as txt:

            soup = BeautifulSoup(txt, 'lxml')
            td_list = list(soup.find_all(class_="sorting_1"))
            
            for td in td_list:
                eliminar_td = re.sub('</td>', "", td.get_text())
                eliminar_td = re.sub('<td class="sorting_1">', "", eliminar_td)
                lista_codigos.append(eliminar_td)

        return lista_codigos