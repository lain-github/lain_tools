#! python3.8
import requests
from bs4 import BeautifulSoup
import pypinyin

def get_youjia(city):
    header = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20100101 Firefox/23.0'}
    url = 'http://youjia.chemcp.com/'
    r = requests.get(url, headers=header).content.decode('GB2312')
    soup = BeautifulSoup(r, 'html.parser')
    allInfo = soup.select("#box > .chem_3 > .cpbox > .cpbaojia > table > tr")[1:32]
    
    youjia =[]
    for i in allInfo:
        area = i.contents[1].contents[0].string
        if city != '' and area != city:
            continue
        v89 = i.contents[3].string
        v92 = i.contents[5].string
        v95 = i.contents[7].string
        v98 = i.contents[9].string
        v0 = i.contents[11].string
        time = i.contents[13].string.replace('/', '-')
        res = '\n'.join(['地区：'+area, '时间：'+time, '89号汽油：'+v89, '92号汽油：'+v92, '95号汽油：'+v95, '98号汽油：'+v98, ' 0号柴油：'+v0, ''])
        youjia.append(res)
    youjia = '\n'.join(youjia)
    return youjia

if __name__ == '__main__':
    print(get_youjia(''))
    print(get_youjia('山东'))