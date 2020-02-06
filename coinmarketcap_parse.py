from bs4 import BeautifulSoup
import pandas as pd
import os
import glob

if not os.path.exists("parsed_files"):
	os.mkdir("parsed_files")

df = pd.DataFrame()

for one_file_name in glob.glob("html_files/*.html"):
	print("parsing: ",one_file_name)
	scraping_time = os.path.basename(one_file_name).replace("coinmarketcap","").replace(".html","")
	f = open(one_file_name,"r")
	soup =  BeautifulSoup(f.read(),'html.parser')
	f.close()

	currencies_table = soup.find("tbody")
	# currencies_row = currencies_table.find("tr")
	currency_rows = currencies_table.find_all("tr")


	for r in currency_rows:
		currency_price = r.find('td',{"class":"cmc-table__cell--sort-by__price"}).find("a").text.replace(",","").replace("$","")
		currency_name = r.find('td',{"class":"cmc-table__cell--sort-by__name"}).find("a",{"class":"cmc-link"}).text
		currency_marketcap = r.find('td',{"class":"cmc-table__cell--sort-by__market-cap"}).find('div').text.replace(",","").replace("$","")
		currency_supply = r.find('td',{"class":"cmc-table__cell--sort-by__circulating-supply"}).find('div').text.replace(" *","").replace(",","")
		df = df.append({
			"time":scraping_time,
			"currency_name":currency_name,
			"currency_price":currency_price,
			"currency_marketcap":currency_marketcap,
			"currency_supply":currency_supply
			},ignore_index=True)
	print(df)
	df.to_csv("parsed_files/coinmarketcap_dataset.csv")




# currencies_table = soup.find("tbody")
# currencies_row = currencies_table.find_all("tr")
# for i in currencies_row:
# 	# price = currencies_row.find('td',{"class":"cmc-table__cell--sort-by__price"}).find("a").text
# 	price = i.find('td',class_="cmc-table__cell--sort-by__price").find("a").get_text()
# 	print(price)