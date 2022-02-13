# coding=gbk
# ^...^*:詹峻
# 开发时间：2022/1/10 14:11
import requests


class Tieba_spider(object):
    def __init__(self, text):
        self.text = text
        self.ur1 = 'https://tieba.baidu.com/f?kw=' + text + '&pn={}'
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36 SLBrowser/7.0.0.12151 SLBChan/103"}

    def get_ur1_list(self):
        """生成ur1列表"""
        ur1_list = [self.ur1.format(i * 50) for i in range(5)]
        return ur1_list

    def get_data_fromurl(self, ur1):
        """从服务器获取数据，并且解码返回"""
        # 这个请求头不能获得完整的HTML内容，可以删除。
        response = requests.get(ur1, headers=self.headers)
        # 此方法可以获得请求浏览器的请求头
        # print(response.request.headers)
        return response.content.decode()

    def save_html(self, html_str, num):
        """保存到本地"""
        file_name = "贴吧_" + text + '第{}页'.format(num) + '.html'
        with open(file_name, 'w', encoding='utf-8') as f:
            f.write(html_str)

    def run(self):
        ur1_list = self.get_ur1_list()
        for item_ur1 in ur1_list:
            html_str = self.get_data_fromurl(item_ur1)
            self.save_html(html_str, ur1_list.index(item_ur1) + 1)


if __name__ == '__main__':
    text = input("请输入贴吧的名字：")
    spider = Tieba_spider(text)
    spider.run()

















    

"""ur1 = 'https://tieba.baidu.com/f?kw={}&pn={}'
text = input("请输入贴吧的名字：")
ur1_list = [ur1.format(text, i * 50) for i in range(5)]
headers = {
    "User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Mobile Safari/537.36 Edg/97.0.1072.55"}

for item_ur1 in ur1_list:
    response = requests.get(item_ur1, headers=headers)

    file_name = "贴吧_" + text + '第{}页'.format(ur1_list.index(item_ur1) + 1) + '.html'
    with open(file_name, 'w', encoding='utf-8') as f:
        f.write(response.content.decode())"""
