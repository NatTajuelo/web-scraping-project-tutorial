import os
from bs4 import BeautifulSoup
import requests
import time
import sqlite3
import matplotlib.pyplot as plt
import seaborn as sns

url = "https://ycharts.com/companies/TSLA/revenues"

headers = 
response = requests.get(url, headers=headers).text



soup = BeautifulSoup(response,"html.parser")
soup