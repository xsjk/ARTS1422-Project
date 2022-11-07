import requests
from bs4 import BeautifulSoup
import re

outFile = open("weatherData.csv", "w", encoding="utf-8")

for month in range(5, 11):

	response = requests.get(
		f"http://tianqihoubao.com/lishi/haikou/month/2017{month:0>2d}.html",
        headers = {
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.134 Safari/537.36 Edg/103.0.1264.71"
        },
        timeout = 5
	)
	soup = BeautifulSoup(response.text, "html.parser")

	for record in soup.find_all("tr")[1:]:
		recordStr = ""
		for field in record.find_all("td"):
			fieldStr = field.text
			fieldStr = re.sub("\s+", '', fieldStr)
			fieldStr = re.sub("℃", 'C', fieldStr)
			recordStr += fieldStr + ","
		outFile.write(recordStr[:-1] + "\n")