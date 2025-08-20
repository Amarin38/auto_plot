import re

from typing import List, Optional
from bs4 import BeautifulSoup

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, WebDriverException

try:
    from config import MAIN_PATH
except ModuleNotFoundError:
    from config import MAIN_PATH


class MaxMinUtils:
    def __init__(self, fecha_desde: str, web: bool, html_file: Optional[str] = None) -> None:
        self.fecha_desde = fecha_desde
        self.html_file = html_file
        self.web = web

    def create_code_list(self, excel: bool) -> List[str]:
        """
        Genera automáticamente la lista de códigos a los que sacarles el máximo y mínimo.
        - Tiene la posibilidad de pasarlo o no a un out.
        """
        lista_final: List[str] = []

        if self.web:
            lista_codigos = self.scrap_web()
        else:
            lista_codigos = self.scrap_local()

        for codigo in lista_codigos:
            lista_final.append(tuple(map(int, codigo.split(".")))) #type: ignore
        
        if excel:
            import pandas as pd

            df = pd.DataFrame({
                "Familia":[fam[0] for fam in lista_final], 
                "Articulo":[art[1] for art in lista_final]
                })
            df.to_excel(f"codigos_maxmin.xlsx")

        return lista_final


    def scrap_web(self) -> List[str]:
        lista_codigos: List[str] = []

        try:
            options = webdriver.FirefoxOptions()
            driver = webdriver.Firefox(options=options)
        except WebDriverException:
            try:
                options = webdriver.ChromeOptions()
                driver = webdriver.Chrome(options=options)
            except WebDriverException:
                options = webdriver.EdgeOptions()
                driver = webdriver.Edge(options=options)

        options.page_load_strategy = 'eager'
        driver.get("https://dota.sistemasanantonio.com.ar/licitaciones/login.aspx")
        
        wait = WebDriverWait(driver, 10) 

        email = driver.find_element(By.NAME, "inputEmail")
        email.send_keys("garantias")
        passwd = driver.find_element(By.NAME, "inputPassword")
        passwd.send_keys("DOTA2024")

        login = driver.find_element(By.ID, "btn_iniciar")
        login.click()
        
        esperar_lici = wait.until(EC.presence_of_element_located((By.XPATH, "//a[@href='#']//div[@class='hover thumbnail']//div[@class='caption']")))

        licitaciones = driver.find_element(By.XPATH, "//a[@href='#']//div[@class='hover thumbnail']//div[@class='caption']")
        licitaciones.click()
        
        esperar_fecha_input = wait.until(EC.presence_of_element_located((By.NAME, "ctl00$MainContent$txt_fecha_desde")))

        try:
            fecha_input = driver.find_element(By.NAME, "ctl00$MainContent$txt_fecha_desde")
        except NoSuchElementException:
            fecha_input = driver.find_element(By.ID, "MainContent_txt_fecha_desde")

        fecha_input.clear()
        fecha_input.send_keys(self.fecha_desde)

        esperar_buscar_boton = wait.until(EC.presence_of_element_located((By.ID, "MainContent_btn_buscar")))

        buscar_boton = driver.find_element(By.ID, "MainContent_btn_buscar")
        buscar_boton.click()

        esperar_busqueda_input = wait.until(EC.presence_of_element_located((By.XPATH, "//input[@type='search']")))

        busqueda_input = driver.find_element(By.XPATH, "//input[@type='search']")
        busqueda_input.clear()
        busqueda_input.send_keys("Finalizada Ningún pedido realizado Pompeya")

        esperar_codigo_lici = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "sorting_1")))

        codigos_licitaciones = driver.find_elements(By.CLASS_NAME, "sorting_1")
        lista_numeros_licitaciones: List[str] = [codigo.text for codigo in codigos_licitaciones]

        for numero in lista_numeros_licitaciones:
            driver.get(f"https://dota.sistemasanantonio.com.ar/licitaciones/licitacion_sel.aspx?id={numero}")

            ordenar_columna = driver.find_element(By.XPATH, "//th[@aria-label='cod: Activar para ordenar la columna de manera ascendente']")
            ordenar_columna.click()

            codigo_repuesto = driver.find_elements(By.CLASS_NAME, "sorting_1")

            lista_codigos += [codigo.text for codigo in codigo_repuesto]
        driver.quit()

        return lista_codigos
    

    def scrap_local(self) -> List[str]:
        lista_codigos: list[str] = []

        with open(f"{MAIN_PATH}/extracted.html", "r") as txt:

            soup = BeautifulSoup(txt, 'lxml')
            td_list = list(soup.find_all(class_="sorting_1"))
            
            for td in td_list:
                eliminar_td = re.sub('</td>', "", td.get_text())
                eliminar_td = re.sub('<td class="sorting_1">', "", eliminar_td)
                lista_codigos.append(eliminar_td)
        return lista_codigos
    

    # def limpiar_codigo(self, codigo: str) -> str:
    #     total_ceros = 5
    #     codigo_spliteado = codigo.split(".")
    #     diferencia_ceros = total_ceros-len(codigo_spliteado[1])
        
    #     return f"{codigo_spliteado[0]}.{"0"*diferencia_ceros}{codigo_spliteado[1]}"  

