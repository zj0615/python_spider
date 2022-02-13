# coding=utf-8
# ^...^*:詹峻
# 开发时间：2022/2/11 9:56
# 这个火车余票查询代码还是可以的，我们完成了查询火车票，将满足期望时间的火车票发送到微信中
# 日后需要完成的任务: （1）可以获得火车票的金额;（2）可以获得期望时间的火车票;（3）可以查询学生票。
import requests
import re
import time


class train_tickets_seacrch(object):
    def __init__(self, date, form_station_name, to_station_name, start_time_low):
        self.headers = {
            "Cookie": "_uab_collina=164454411272438220438461; JSESSIONID=8C9CF62227E56B3A5A9FFA3AFA5F3DB3; RAIL_DEVICEID=s8AoCOwLzukkQV9ReNfXocYD_1A5jrW0TalMK8sIrQw4bKgWdk7Ef1t2tTz2aphoLYuElo04hEg9ucaHTcnELNZofizEpl0GlZP2NyEuNjazYnnbtRymM077HcAE2644owAGX7wnILQkeXLXhPBneNW-OpsE1GXK; RAIL_EXPIRATION=1644872859236; guidesStatus=off; highContrastMode=defaltMode; cursorStatus=off; _jc_save_fromStation=%u4E0A%u6D77%2CSHH; _jc_save_toStation=%u6EA7%u9633%2CLEH; _jc_save_toDate=2022-02-11; _jc_save_wfdc_flag=dc; _jc_save_fromDate=2022-02-20; _jc_save_zwdch_fromStation=%u5317%u4EAC%2CBJP; _jc_save_zwdch_cxlx=0; BIGipServerpassport=904397066.50215.0000; route=c5c62a339e7744272a54643b3be5bf64; BIGipServerotn=1373176074.24610.0000",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.80 Safari/537.36 Edg/98.0.1108.43"
        }
        # 12306的城市名和城市代码js文件URL
        self.js_url = 'https://kyfw.12306.cn/otn/resources/js/framework/station_name.js?station_version=1.9061'
        # 向sever酱发送的URL匹配格式
        self.server_url = 'https://sctapi.ftqq.com/SCT119946ToXLl4pDZSiyWDU0xsSHDPR5O.send?text=%s&desp=%s'
        self.date = date
        self.form_station_name = form_station_name
        self.to_station_name = to_station_name
        self.start_time_low = start_time_low

    # 调用server酱,推送到微信
    def send_msg(self, title, info):
        url = self.server_url % (title, info)
        requests.get(url)

    # 获得火车站点代码
    def get_station(self):
        r = requests.get(self.js_url, verify=False)
        pattern = u'([\u4e00-\u9fa5]+)\|([A-Z]+)'
        result = re.findall(pattern, r.text)
        station = dict(result)
        return station

    # 生成查询的url
    def get_query_url(self, text):
        # 城市名代码查询字典
        # key : 城市名 value : 城市代码
        try:
            date = self.date
            form_station_name = self.form_station_name
            to_station_name = self.to_station_name
            # 将城市名转换为代码
            from_station = text[form_station_name]
            to_station = text[to_station_name]
        except:
            date, from_station, to_station = '--', '--', '--'
        # API URL 构造
        url = (
            'https://kyfw.12306.cn/otn/leftTicket/queryA?'
            'leftTicketDTO.train_date={}&'
            'leftTicketDTO.from_station={}&'
            'leftTicketDTO.to_station={}&'
            'purpose_codes=ADULT'
        ).format(date, from_station, to_station)
        # print(url)
        return url

    # 比较期望时间和实际时间的大小
    def time_map(self, start_time, start_time_low):
        time1 = time.strptime(start_time, "%H:%M")
        time2 = time.strptime(start_time_low, "%H:%M")
        # print(time1,' ',time2)
        if time1 <= time2:
            return True
        else:
            return False

    # 获取车次信息
    def query_train_info(self, url):
        try:
            r = requests.get(url, headers=self.headers)
            # 获得返回json数据中data字段的result结果
            r.encoding = 'utf-8'
            # print(r.status_code)
            raw_trains = r.json()['data']['result']
            # print(raw_trains)
            flag = 0
            count = len(raw_trains)
            count_time = 0
            for raw_train in raw_trains:
                count_time += 1
                data_list = raw_train.split('|')
                # 车次号码
                train_no = data_list[3]
                # 出发站
                from_station_code = data_list[6]
                from_station_name = from_station_code + ' | ' + self.form_station_name
                # 终点站
                to_station_code = data_list[7]
                to_station_name = to_station_code + ' | ' + self.to_station_name
                # 出发时间
                start_time = data_list[8]
                # 到达时间
                arrive_time = data_list[9]
                # 总耗时
                time_fucked_up = data_list[10]
                # 一等座
                first_class_seat = data_list[31] or '--'
                # 二等座
                second_class_seat = data_list[30] or '--'
                # 软卧
                soft_sleep = data_list[23] or '--'
                # 硬卧
                hard_sleep = data_list[28] or '--'
                # 硬座
                hard_seat = data_list[29] or '--'
                # 无座
                no_seat = data_list[26] or '--'

                # 打印查询结果
                info = (
                    '车次:{}\n出发站:{}\n目的地:{}\n出发时间:{}\n到达时间:{}\n消耗时间:{}\n座位情况：\n一等座：「{}」 \n二等座：「{}」\n软卧：「{}」\n硬卧：「{}」\n硬座：「{}」\n无座：「{}」\n\n'.format(
                        train_no, from_station_name, to_station_name, start_time, arrive_time, time_fucked_up,
                        first_class_seat,
                        second_class_seat, soft_sleep, hard_sleep, hard_seat, no_seat))
                print(info)
                # 通过server酱发送微信消息
                if (second_class_seat != '无' or first_class_seat!='无') and self.time_map(start_time, self.start_time_low) and count_time <= 5:
                    self.send_msg("%s次高铁有票了" % (start_time+'--'+train_no), info)
                    flag = 1
                else:
                    continue
                # 如果通过server酱发送微信和打印全部信息后退出，否则不输出
                if flag == 1 and count == count_time:
                    return True
        except Exception as e:
            print(e)


if __name__ == '__main__':
    # 关闭https证书验证警告
    requests.packages.urllib3.disable_warnings()
    # 一些基本输入
    date = input("请输入车票时间(xxxx-xx-xx):")
    form_station_name = input("请输入出发站:")
    to_station_name = input("请输入终点站:")
    time_count = int(input("请输入最多查询次数:"))
    start_time_low = input("请输入最低时间(xx:xx):")
    # 初始化
    search = train_tickets_seacrch(date, form_station_name, to_station_name, start_time_low)
    # 获得火车站点代码
    text = search.get_station()
    # 获得访问URL
    url = search.get_query_url(text)
    # 循环查询，直到查询到想要的车次有票终止
    time_no = 0
    while True:
        time.sleep(1)  # 刷票频率
        time_no += 1
        if search.query_train_info(url) or time_count == time_no:
            break
