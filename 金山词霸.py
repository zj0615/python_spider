# coding=utf-8
# ^...^*:詹峻
# 开发时间：2022/1/11 14:22

# takeResult: function(e)
# {
#     var
# t = f().parse(e)
# , r = c()(
#     "6key_cibaifanyicjbysdlove1".concat(t.q.replace( / (^ \s *) | (\s * $) / g, ""))).toString().substring(0,
#                                                                                                            16);
# return h("/index.php?c=trans&m=fy&client=6&auth_user=key_ciba&sign=".concat(r), {
#     baseURL: "//ifanyi.iciba.com",
#     method: "post",
#     headers: {
#         "Content-Type": "application/x-www-form-urlencoded"
#     },
#     data: e
# })
# },

import hashlib
import json
import requests
# 使用谷歌的语言识别库，
from langdetect import detect
from langdetect import detect_langs
from langdetect import DetectorFactory


class fy_spider(object):
    def __init__(self, query_str):
        self.query_str = query_str
        # 初始化翻译路径
        sign = (hashlib.md5(("6key_cibaifanyicjbysdlove1" + self.query_str).encode('utf-8')).hexdigest())[0:16]
        ur1 = 'http://ifanyi.iciba.com/index.php?c=trans&m=fy&client=6&auth_user=key_ciba'
        self.ur1 = ur1 + '&sign=' + sign
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36 Edg/97.0.1072.55"}
        # 获取请求体数据
        self.data = self.get_data(query_str)

    def get_data(self, query_str):
        """获取请求体内容"""
        DetectorFactory.seed = 0  # 让识别结果唯一。
        sr = detect(query_str)
        print('识别语种为：', sr)  # 打印识别的语言
        print('正确概率为：', detect_langs(sr))  # 打印识别语言的概率。
        # if input('输入是否正确（yes or no）：') == 'no':
        #     sr = input('输入正确语言：')
        sc = input("请输入翻译语言：")
        data = {
            'from': sr,
            'to': sc,
            'q': self.query_str
        }
        return data

    def get_data_fromurl(self):
        """从服务器获取数据，并且解码返回"""
        # 这个请求头不能获得完整的HTML内容，可以删除。
        response = requests.post(self.ur1, headers=self.headers, data=self.data)
        # 此方法可以获得请求浏览器的请求头
        # print(response.request.headers)
        return response.content.decode('utf-8')

    def parse_data(self, json_str):
        dict_data = json.loads(json_str)
        result = dict_data['content']['out']
        # result=result.encode('utf-8')
        print('{}\n翻译后的结果是:\n{}'.format(self.query_str, result))

    def run(self):
        # 1.获取URL 请求头 请求体
        # 2.发起请求获取相应数据
        json_str = self.get_data_fromurl()
        # 提取数据
        self.parse_data(json_str)


if __name__ == '__main__':
    print('中文：zh ||', '英语：en ||', '日语：ja ||', '德语：de ||', '法语：fr ||', '西班牙语：es ||', '韩语：ko')
    query_str = input("请输入要翻译的内容：")
    spider = fy_spider(query_str)
    spider.run()
