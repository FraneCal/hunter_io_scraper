from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

URL = "https://hunter.io/search"

driver = webdriver.Chrome()
driver.get(URL)

email_input = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="email-field"]')))
email_input.send_keys('EMAIL')

password_input = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="password-field"]')))
password_input.send_keys('PASSWORD')

log_in_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="signin_form"]/div[2]/button[2]')))
log_in_button.click()

time.sleep(5)

page_source = driver.page_source

driver.quit()

soup = BeautifulSoup(page_source, "html.parser")
