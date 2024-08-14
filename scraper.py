from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
import pandas as pd
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
    
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'ds-result__data')))
    
    page_source = driver.page_source
    
    soup = BeautifulSoup(page_source, "html.parser")
    boxes = soup.find_all('div', class_='ds-result__data')

    results = []
    
    for box in boxes:
        try:
            full_name = box.find('div', class_='ds-result__fullname').getText()
        except (NoSuchElementException, AttributeError):
            full_name = None
        
        try:
            email = box.find('div', class_='ds-result__email').getText()
        except (NoSuchElementException, AttributeError):
            email = None 
        
        try:
            title = box.find('div', class_='ds-result__attribute').getText().strip()
        except (NoSuchElementException, AttributeError):
            title = None 
        
        try:
            linkedin_link = box.find('a', {'aria-label': lambda value: value and 'LinkedIn' in value})
            linkedin = linkedin_link.get('href') if linkedin_link else None
        except (NoSuchElementException, AttributeError):
            linkedin = None 
        
        try:
            twitter_link = box.find('a', {'aria-label': lambda value: value and 'Twitter' in value})
            twitter = twitter_link.get('href') if twitter_link else None
        except (NoSuchElementException, AttributeError):
            twitter = None 
        
        # Append to results list
        results.append({
            'Full Name': full_name,
            'Email': email,
            'Title': title,
            'LinkedIn': linkedin,
            'Twitter': twitter
        })
    
    # Convert results to DataFrame
    df = pd.DataFrame(results)
    return df

if __name__ == "__main__":

    URL = "https://hunter.io/search"
    
    email = 'YOUR EMAIL'
    password = 'YOUR PASSWORD'
    
    driver = setup_webdriver()
    
    login(email, password, URL, driver)
    
    company_domain = 'COMPANY DOMAIN YOU ARE SEARCHING FOR'
    
    results_df = search_company(company_domain)
    
    # Save results to Excel
    results_df.to_excel('data.xlsx', index=False)

    print("Scraping successful! Data has been saved to 'data.xlsx'.")

    driver.quit()
