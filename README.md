# UE
pip install scrapy
pip install requests
pip install pandas
from scrapy import Selector
import requests
import pandas as pd
url = 'https://www.ubereats.com/store/uber-eats-%E5%84%AA%E5%B8%82-%E4%B8%AD%E5%B1%B1%E5%BA%97/D8gZ3fpOQW6HoX5tCxhi1A?diningMode=DELIVERY&pl=JTdCJTIyYWRkcmVzcyUyMiUzQSUyMkdsb2JhbCUyME1hbGwlMjBaaG9uZ2hlJTIwU3RvcmUlMjIlMkMlMjJyZWZlcmVuY2UlMjIlM0ElMjJDaElKT1cxOFNTZW9RalFSNW9CRGwxeFN3UWslMjIlMkMlMjJyZWZlcmVuY2VUeXBlJTIyJTNBJTIyZ29vZ2xlX3BsYWNlcyUyMiUyQyUyMmxhdGl0dWRlJTIyJTNBMjUuMDA2MTA1MiUyQyUyMmxvbmdpdHVkZSUyMiUzQTEyMS40NzUxMzY2JTdE'
html = requests.get(url).content
sel = Selector(text=html)
href = sel.xpath('//*[@id="main-content"]/div[5]/div[3]/div[2]/div[1]/div[2]/div/div/nav/div/a/@href').extract()
print(href)

dc_dict = dict()

for h in href:
    html = requests.get('https://www.ubereats.com/'+h).content
    sel = Selector(text=html)
    product = sel.xpath('//*[@id="main-content"]/div[5]/ul/li/ul/li/div/div/div[2]/div/h4/div/text()').extract()
    price = sel.xpath( '//*[@id="main-content"]/div[5]/ul/li/ul/li/div/div/div[2]/text()').extract()
    for pro, pri in zip(product, price):
        dc_dict[pro] = pri
df = pd.DataFrame(dc_dict, index=[0])
df = df.T
df.to_csv('0103.csv',encoding="utf_8_sig")
