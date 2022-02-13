# coding=utf-8
# ^...^*:詹峻
# 开发时间：2022/1/15 10:13
import requests
import time
import os


class Image(object):
    def __init__(self):
        self.url = 'https://image.baidu.com/search/acjson?'
        self.headers = {
            'Cookie': 'BDqhfp=%25B8%25DF%25C7%25E5%25CD%25BC%25C6%25AC%26%26NaN-1undefined%26%260%26%261; BIDUPSID=4E8DBCD97714440B03463BF2C9DFDA7D; PSTM=1641301755; BAIDUID=4E8DBCD97714440B29F9CC449359EDCB:FG=1; MCITY=-348%3A; H_WISE_SIDS=107319_110085_127969_132550_174441_179347_184716_185268_186635_187726_188331_188468_189326_189731_189755_190247_190627_191068_191256_191369_191371_192206_192351_192957_193283_193557_194038_194085_194519_194583_195107_195342_195477_195538_195632_195679_195757_196046_196049_196425_196514_196518_197004_197241_197286_197552_197579_197711_197782_197831_198079_198121_198189_198256_198418_198420_198511_198537_198591_198650_198663_198876_198930_198998_199162_199177_199286_199305_199466_199575_199752_199795_199878_199981_200042_200055_200194_200273_200451_200551; BAIDUID_BFESS=4E8DBCD97714440B29F9CC449359EDCB:FG=1; BDORZ=FFFB88E999055A3F8A630C64834BD6D0; BDRCVFR[59pT2yMJfIY]=I67x6TjHwwYf0; delPer=0; PSINO=3; H_PS_PSSID=31253_26350; BA_HECTOR=a124012l8h0l802gdp1gu4b8v0q; BDRCVFR[dG2JNJb_ajR]=mk3SLVN4HKm; userFrom=ala; BDRCVFR[-pGxjrCMryR]=mk3SLVN4HKm',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36 Edg/97.0.1072.62 '
        }
        self.params = {
            'tn': 'resultjson_com',
            'logid': '9018427335155613970',  # 此参数没有影响
            'ipn': 'rj',
            'ct': '201326592',
            'is': '',
            'fp': 'result',
            'fr': 'ala',
            'word': '',
            'queryWord': '',
            'cl': '2',
            'lm': '-1',
            'ie': 'utf - 8',
            'oe': 'utf - 8',
            'adpicid': '',
            'st': '',
            'z': '',
            'ic': '',
            'hd': '',
            'latest': '',
            'copyright': '',
            's': '',
            'se': '',
            'tab': '',
            'width': '',
            'height': '',
            'face': '',
            'istype': '',
            'qc': '',
            'nc': '',
            'expermode': '',
            'nojc': '',
            'isAsync': '',
            'pn': '',
            'rn': '30',
            'gsm': '',
            'time': ''
        }
        self.image_list = []  # 用来保存爬取图片的URL路径

    def get_image(self, num):
        start = int(input('请输入开始页数:'))-1
        for i in range(start, num+start):
            self.params['time'] = int(time.time() * 100)  # 应用time模块获得实时的时间戳
            self.params['pn'] = i * 30  # 爬取图片的页数
            name = input('请输入图片类型：')  # 爬取图片的类型
            self.params['word'] = self.params['queryWord'] = name
            response = requests.get(url=self.url, headers=self.headers, params=self.params)  # 获得网页的HTML
            for j in range(0, len(response.json()['data']) - 1):  # 遍历获得图片的URL
                self.image_list.append(response.json()['data'][j]['thumbURL'])

    def save_image(self, numbers):
        n = 1
        filecount = 0
        for root, dir, files in os.walk("E:/pythonSpider/图片"):  # 获得文件下的文件数量
            filecount += len(files)
        n += filecount
        for i in self.image_list[0:numbers]:  # 遍历URL列表读取数据，写入文件中
            image = requests.get(url=i)
            with open('./图片/{}.jpg'.format(n), 'wb') as f:
                f.write(image.content)
            n += 1


if __name__ == '__main__':
    image = Image()
    numbers = int(input('请输入爬取的数量：'))
    num = (numbers // 30) + 1
    if numbers % 30 == 0:
        num -= 1
    image.get_image(num)
    image.save_image(numbers)
