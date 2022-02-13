# coding=utf-8
# ^...^*:詹峻
# 开发时间：2022/2/12 9:13
from bs4 import BeautifulSoup
import requests
import csv
import re


def getlocation(name):  # 调用百度API查询位置
    bdurl = 'http://api.map.baidu.com/geocoder/v2/?address='
    output = 'json'
    # ak='你的密匙'#输入你刚才申请的密匙
    ak = 'VMfQrafP4qa4VFgPsbm4SwBCoigg6ESN'  # 输入你刚才申请的密匙
    callback = 'showLocation'
    uri = bdurl + name + '&output=t' + output + '&ak=' + ak + '&callback=' + callback + '&city=沈阳'
    # print(uri)
    res = requests.get(uri)
    s = BeautifulSoup(res.text, 'lxml')
    lng = s.find('lng')
    lat = s.find('lat')
    if lng:
        return lng.get_text() + ',' + lat.get_text()


url = 'https://sy.lianjia.com/ershoufang/pg'
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.80 Safari/537.36 Edg/98.0.1108.43"
}
page = list(range(0, 101, 1))
p = []
hi = []
fi = []
name_all = []
for i in page:
    print(i)
    response = requests.get(url + str(i), headers=headers, timeout=5)
    response.encoding = 'utf-8'
    soup = BeautifulSoup(response.text, 'lxml')
    # 提取价格
    prices = soup.find_all('div', class_='priceInfo')
    for price in prices:
        p.append(price.span.string)
    # 提取房源信息
    na = soup.find_all('div', class_='positionInfo')
    for n in na:
        name_all.append(n.a.string)
    hs = soup.find_all('div', class_='houseInfo')
    for h in hs:
        hi.append(h.get_text())
    # 提取关注度
    followInfo = soup.find_all('div', class_='followInfo')
    for f in followInfo:
        fi.append(f.get_text())

n = 0
num = len(p)
file = open('syfj.csv', 'w', newline='', encoding='utf-8')
headers = ['name', 'loc', 'style', 'size', 'price', 'foc']
writers = csv.DictWriter(file, headers)
writers.writeheader()
while n < num:
    print(n)
    h0 = hi[n].split('|')
    name = name_all[n]
    loc = getlocation(name)
    style = re.findall(r'\s?\d.\d.\s', hi[n])
    if style:
        style = style[0]
    size = re.findall(r'\s\d+\.?\d+', hi[n])
    if size:
        size = size[0]
    price = p[n]
    foc = re.findall(r'^\d+', fi[n])[0]
    house = {
        'name': '',
        'loc': '',
        'style': '',
        'size': '',
        'price': '',
        'foc': ''
    }
    # 将房子的信息放进一个dict中
    house['name'] = name
    house['loc'] = loc
    house['style'] = style
    house['size'] = size
    house['price'] = price
    house['foc'] = foc
    # print(house)
    try:
        writers.writerow(house)  # 将dict写入到csv文件中
    except Exception as e:
        print(e)
        # continue
    n += 1
file.close()
