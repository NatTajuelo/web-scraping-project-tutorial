import sqlite3
import time
from bs4 import BeautifulSoup
import requests
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

#Importar el URL 
url = "https://ycharts.com/companies/TSLA/revenues"
html_info = requests.get(url, time.sleep(10)).text

#Descarga del HTML
headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36"}
response = requests.get(url, headers=headers)
html_info = response.text

#Transformación del HTML
soup = BeautifulSoup(html_info,"html.parser")
print(soup)

#Buscar y trabajar con las tablas (creación de la base de datos)
tables = soup.find_all("table")

dates = [row.find_all("td")[0].text.strip() for table in tables for row in table.find("tbody").find_all("tr")]
values = [row.find_all("td")[1].text.strip() for table in tables for row in table.find("tbody").find_all("tr")]

df = pd.DataFrame({"Date": dates, "Revenue": values})

df = df.replace({",": "", "B": ""}, regex=True).dropna()
pd.set_option("display.max_columns", None)

df_filtro = df[df["Date"].str.contains(r'\w{3,9}\s\d{2}\s\d{4}', regex=True)]
print(df_filtro)

df_filtro = df_filtro[df_filtro["Revenue"] != ""]
df_filtro.head()

# Almacenar en SQLite

connection = sqlite3.connect("Tesla.db")

cursor = connection.cursor()
cursor.execute("""CREATE TABLE revenue (Date, Revenue)""")

tesla_tuples = list(df_filtro.to_records(index = False))
tesla_tuples[:5]

cursor.executemany("INSERT INTO revenue VALUES (?,?)", tesla_tuples)
connection.commit()

for row in cursor.execute("SELECT * FROM revenue"):
    print(row)

#Serie de tiempo

fig, axis = plt.subplots(figsize = (10, 5))

df_filtro["Date"] = pd.to_datetime(df_filtro["Date"])
df_filtro["Revenue"] = pd.to_numeric(df_filtro["Revenue"], errors='coerce')
df_filtro["Revenue"] = df_filtro["Revenue"].fillna(0).astype(int)
sns.lineplot(data = df_filtro, x = "Date", y = "Revenue")

plt.tight_layout()

plt.show()

#Beneficio anual

fig, axis = plt.subplots(figsize = (10, 5))

df_filtro["Date"] = pd.to_datetime(df_filtro["Date"])
tesla_revenue_yearly = df_filtro.groupby(df_filtro["Date"].dt.year)["Revenue"].sum().reset_index()

sns.barplot(data = tesla_revenue_yearly[tesla_revenue_yearly["Date"] < 2023], x = "Date", y = "Revenue", palette="flare")

plt.tight_layout()

plt.show()

#Beneficio mensual

fig, axis = plt.subplots(figsize = (10, 5))

tesla_revenue_monthly = df_filtro.groupby(df_filtro["Date"].dt.month)["Revenue"].sum().reset_index()

sns.barplot(data = tesla_revenue_monthly, x = "Date", y = "Revenue", palette="light:#5A9")

plt.tight_layout()

plt.show()

# En el archivo explore.es.ipynb se pueden ver los gráficos #