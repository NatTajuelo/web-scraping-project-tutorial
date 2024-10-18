from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import pandas as pd


service = Service('')  
driver = webdriver.Chrome(service=service)

url = "https://ycharts.com/companies/TSLA/revenues"
driver.get(url)

table = driver.find_element(By.TAG_NAME, 'table')
rows = table.find_elements(By.TAG_NAME, 'tr')

data = []
for row in rows:
    cols = row.find_elements(By.TAG_NAME, 'td')
    cols = [col.text for col in cols]
    data.append(cols)

driver.quit()

df = pd.DataFrame(data, columns=['Date', 'Revenue'])
print(df)