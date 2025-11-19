from selenium import webdriver

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as exp_cond

from selenium.common.exceptions import WebDriverException

class ScrapUtils:
    @staticmethod
    def create_page_licitaciones() -> tuple:
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

        return driver, wait
    

    def login_licitaciones(self) -> tuple:
        driver, wait = self.create_page_licitaciones()
        
        self.wait_by_name(wait, "inputEmail")
        self.wait_by_name(wait, "inputPassword")

        email = driver.find_element(By.NAME, "inputEmail")
        email.send_keys("garantias")
        passwd = driver.find_element(By.NAME, "inputPassword")
        passwd.send_keys("DOTA2024")

        self.wait_by_id(wait, "btn_iniciar")
        login = driver.find_element(By.ID, "btn_iniciar")
        login.click()
        
        self.wait_by_xpath(wait, "//a[@href='#']//div[@class='hover_unified thumbnail']//div[@class='caption']")
        licitaciones = driver.find_element(By.XPATH, "//a[@href='#']//div[@class='hover_unified thumbnail']//div[@class='caption']")
        licitaciones.click()

        return driver, wait
    

    @staticmethod
    def wait_by_name(wait, name: str):
        return wait.until(exp_cond.presence_of_element_located((By.NAME, name)))
    
    @staticmethod
    def wait_by_xpath(wait, name: str):
        return wait.until(exp_cond.presence_of_element_located((By.XPATH, name)))

    @staticmethod
    def wait_by_id(wait, name: str):
        return wait.until(exp_cond.presence_of_element_located((By.ID, name)))
    
    @staticmethod
    def wait_by_class(wait, name: str):
        return wait.until(exp_cond.presence_of_element_located((By.CLASS_NAME, name)))

    @staticmethod
    def wait_by_css(wait, name: str):
        return wait.until(exp_cond.presence_of_element_located((By.CSS_SELECTOR, name)))
