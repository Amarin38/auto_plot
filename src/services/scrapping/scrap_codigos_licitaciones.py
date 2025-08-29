import pandas as pd

from typing import List

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from ..utils.scrap_utils import ScrapUtils
from ..utils.exception_utils import execute_safely

class ScrapCodigosLicitaciones:
    def __init__(self, text: str) -> None:
        self.text = text
    
    @execute_safely
    def scrap(self) -> zip:
        driver, wait = ScrapUtils().login_licitaciones() # type: ignore

        ScrapUtils.wait_by_xpath(wait, "//a[@id='MainContent_btn_add']")
        agregar_licitaciones = driver.find_element(By.XPATH, "//a[@id='MainContent_btn_add']")
        agregar_licitaciones.click()

        ScrapUtils.wait_by_id(wait, "MainContent_txt_art")
        buscar_codigo = driver.find_element(By.ID, "MainContent_txt_art")
        buscar_codigo.send_keys(self.text, Keys.ENTER)

        ScrapUtils.wait_by_class(wait, "sorting_1")
        codigos_licitaciones = driver.find_elements(By.CLASS_NAME, "sorting_1")
        ScrapUtils.wait_by_css(wait, "td:nth-child(2)")
        nombres_licitaciones = driver.find_elements(By.CSS_SELECTOR, "td:nth-child(2)")
        
        lista_numeros_licitaciones: List[str] = [codigo.text for codigo in codigos_licitaciones]
        lista_nombres_licitaciones: List[str] = [nombre.text for nombre in nombres_licitaciones]
        
        driver.close()

        return zip(lista_numeros_licitaciones, lista_nombres_licitaciones)


    def scrap_to_df(self) -> None:
        pd.DataFrame(self.scrap(), columns=["Codigo", "Nombre"]).to_excel("codigos_licitaciones.xlsx")
        