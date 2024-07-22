from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time


def setup_webdriver():
    driver = webdriver.Chrome()
    driver.maximize_window()
    return driver

def login(email, password, URL, driver): 
    driver.get(URL)

    email_input = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="email-field"]')))
    email_input.send_keys(email)

    password_input = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="password-field"]')))
    password_input.send_keys(password)

    log_in_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="signin_form"]/div[2]/button[2]')))
    log_in_button.click()

def search_company(company_domain):
    domain_search = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="domain-field"]')))
    domain_search.send_keys(company_domain)
    domain_search.send_keys(Keys.ENTER)

    time.sleep(5)

    page_source = driver.page_source

    soup = BeautifulSoup(page_source, "html.parser")

    results = soup.find('div', class_='ds-result__primary').getText()
    print(results)
    
if __name__ == "__main__":

    URL = "https://hunter.io/search"

    email = 'EMAIL'
    password = 'PASSWORD'

    driver = setup_webdriver()

    login(email, password, URL, driver)

    company_domain = 'COMPANY DOMAIN'

    search_company(company_domain)

    driver.quit()
