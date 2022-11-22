#! python3.8
import requests
import json

def get_iciba_everyday():
    url = 'http://open.iciba.com/dsapi/'
    r = requests.get(url)
    all = json.loads(r.text)
    #print(all)
    english = all['content']
    chinese = all['note']
    soup = english+'\n'+chinese
    return soup

if __name__ == '__main__':
    print(get_iciba_everyday())