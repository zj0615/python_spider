# coding=gbk
# ^...^*:ղ��
# ����ʱ�䣺2022/1/8 9:30
import lxml.html, requests
# lxml����������xml��HTML�Ĺ��߿���ʹ��Xpath��CSS����λԪ��
# requests��python http��

ur1 = 'https://www.python.org/dev/peps/pep-0020'  # һ����ҳ������
xpath = '//*[@id="the-zen-of-python"]/pre/text()'  # ��һ��xpath·�����ʽ
res = requests.get(ur1)  # ��url����һ��http get���󣬷���ֵ������res
ht = lxml.html.fromstring(res.text)
text = ht.xpath(xpath)  # ʹ��xpath����λHTMlElement�е���Ϣ
print('Hello,\n' + ''.join(text))
