import os
from bs4 import BeautifulSoup
import requests
import time
import sqlite3
import matplotlib.pyplot as plt
import seaborn as sns

url = "https://ycharts.com/companies/TSLA/revenues"
html_info = requests.get(url).text

if "403 Forbidden" in html_info:
    headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36"}
    response = requests.get(url, headers=headers)
    html_info = response.text

soup = BeautifulSoup(html_info,"html.parser")
print(soup)

tables = soup.find_all("table")