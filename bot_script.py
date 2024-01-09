import pandas as pd
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver 
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service = service)

driver.get("https://web.whatsapp.com/")

wait = WebDriverWait(driver, timeout = 60)
barra_lateral = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id = "side"]')))
barra_lateral = driver.find_element(By.XPATH, value = '//*[@id = "side"]')