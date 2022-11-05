import requests
from bs4 import BeautifulSoup
import re

outFile = open("weatherData.csv", "w", encoding="utf-8")

for month in range(5, 11):

	response = requests.get(f"http://tianqihoubao.com/lishi/haikou/month/2017{month:0>2d}.html")
	soup = BeautifulSoup(response.text, "html.parser")

	for record in soup.find_all("tr")[1:]:
		recordStr = ""
		for field in record.find_all("td"):
			fieldStr = field.text
			fieldStr = re.sub("\s+", '', fieldStr)
			fieldStr = re.sub("℃", 'C', fieldStr)
			recordStr += fieldStr + ","
		outFile.write(recordStr[:-1] + "\n")