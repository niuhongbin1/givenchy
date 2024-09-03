'''
传入种类 url 获得产品详情页  url 
'''


import requests
from lxml import etree
import time 
import re
import json
import logging
 


def requ_repeat(link,err_txt,par=None):
    """ 用于多次重试

    Args:
        link (_type_): _description_
        err_txt (_type_): _description_

    Returns:
        _type_: _description_
    """
    keep = True
    maxtimes = 6
    count = 0
    while keep and count < maxtimes:
        try:
            hes = {
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
                # 'client_id':'607e3016889f431fb8020693311016c9',
                # 'client_secret':'60bbcdcD722D411B88cBb72C8246a22F',
                # # 'content-type': 'application/json',
                # 'origin': 'chrome-extension://ieoejemkppmjcdfbnfphhpbfmallhfnc',
                # 'cookie': 'lv-dispatch=fra-fr'
            }

            response = requests.request("GET",link,timeout=5,params=par,headers=hes)
            
            if response.status_code == 200:
                keep = False
                return response
            else:
                count = count + 1
                print(link+err_txt+'  获取重试' + str(count))
                pass
        except Exception as e:
            # print(e,link)
            count = count + 1
            print(err_txt+'  获取重试' + str(count))
        
    return False


def re_pid(t):
    
    return t["hits"]

def data(a,b,url):
    
    
    url = url+'?start='+str(a)+'&sz='+str(b)


    
    try:
        response = requ_repeat(link=url,err_txt='获取产品列表')
        if response == False:
            return [False,False]
        p_html = etree.HTML(response.text)
        pids = p_html.xpath('//div[@class="search-results-content productgrid"]/ul/li')
        if len(pids) == 20:
            next = True
            pass
        else:
            next = False
            pass
        return [pids,next]
    except:
        print('获取产品列表失败',url,'resson --> internet')
        print('record this url so coder can deal with it easily')
        return [False,False]


def re_cgid(t):
    """get cgid 

    Args:
        t (str): html

    Returns:
        _type_: str
    """
    mod = re.compile('data-category-code="(.*?)"')
    try:
        s = mod.findall(t)[0]
        return s 
    except:
        return False


def get_cgid(url):
    try:
        response = requ_repeat(link=url,err_txt='获取  cgid')
        if response == False:
            return False
        cgid = re_cgid(response.text)
        if cgid == False:
            return False
        return cgid
    except:
        return False

def get_name(p):
    
    return p['productName']


def get_pr(p):
    
    return p["rawPrice"][:-2]


def pos(p_html):
    pdds = [] 
    lis1 = p_html
    
    for i in lis1:
        try:
            url = i.xpath('./div/figure/a/@href')[0]
            
            pdds.append(url)
            pass
        except:
            continue
    

        
    return pdds

            


def main(url):
    # cgid = get_cgid(url)
    a = 0 
    b = 20
    pdds = []
    while True:
        jus = data(a,b,url)
        if jus[0] == False:
            break
        else:
            pdds = pdds + pos(jus[0])
            if jus[1] == False:
                break
            else: 
                a = a+20
                pass
            pass
        pass
    return pdds
        
        
        
def out(url):
    print('-----------  print  ----------')
    return main(url)

if __name__ == '__main__':
    # url
     out('https://www.givenchy.com/fr/fr/homme/pret-a-porter/chemises/')