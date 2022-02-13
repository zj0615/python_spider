# coding=gbk
# ^...^*:詹峻
# 开发时间：2022/1/8 9:30
import lxml.html, requests
# lxml是用来解析xml和HTML的工具可以使用Xpath和CSS来定位元素
# requests是python http库

ur1 = 'https://www.python.org/dev/peps/pep-0020'  # 一个网页的链接
xpath = '//*[@id="the-zen-of-python"]/pre/text()'  # 是一个xpath路径表达式
res = requests.get(ur1)  # 对url发送一个http get请求，返回值被赋予res
ht = lxml.html.fromstring(res.text)
text = ht.xpath(xpath)  # 使用xpath来定位HTMlElement中的信息
print('Hello,\n' + ''.join(text))
