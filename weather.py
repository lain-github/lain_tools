#! python3.8
import requests
from bs4 import BeautifulSoup
import pypinyin

def get_pinyin(city):
    result = pypinyin.pinyin(city, style=pypinyin.NORMAL)
    res = ''
    for i in result:
        res = res + i[0]

    return res

def get_weather(city):
    city_pinyin = get_pinyin(city)
    # 声明头，模拟真人操作，防止被反爬虫发现
    header = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20100101 Firefox/23.0'}
    # 通过传入的城市名拼音参数来拼接出该城市的天气预报的网页地址
    website = "http://www.tianqi.com/" + city_pinyin + ".html"
    html = requests.get(website,headers=header).text
    soup = BeautifulSoup(html, "html.parser")
    # html.parser表示解析使用的解析器
    nodes = soup.find_all('dd')
    tody_weather = ""
    for node in nodes: # 遍历获取各项数据
        temp = node.get_text()
        if (temp.find('[切换城市]')):
            temp = temp[:temp.find('[切换城市]')]
        tody_weather += temp
    # 去除字符串中的空行:
    tianqi = " ".join([s for s in tody_weather.splitlines(True) if s.strip()])

    return tianqi

if __name__ == '__main__':
    print(get_weather('qingdao'))
    print(get_weather('huangdao'))