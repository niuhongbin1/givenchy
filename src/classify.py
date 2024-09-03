import time
import requests
from lxml import etree




def get_html_404():
    # curl = 'https://www.givenchy.com/fr/fr/homepage'
    # hs = {
    # 'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
    # }
    # rep = requests.get(url=curl,timeout=5,headers=hs)
    # text = rep.text
    with open('./c.html',mode='r',encoding='utf-8') as t:
        text = t.read()
    p_html = etree.HTML(text)
    
    # p_html= p_html1.xpath('//div[@class="lv-mega-menu__content"]/div/ul')[0]
    ds = xml_to_dict(p_html)
    
    return ds

  
def xml_to_dict(p):
    root = []
    lis0  = p.xpath('//ul[@class="level-1"]/li')
    lis = [lis0[0],lis0[1]]
    for i in lis:
        name = i.xpath('./a/span/text()')
        if len(name) != 0:
            ff = {
                'name':name[0].replace('\n','').replace(' ',''),
                'data-url':None,
                'cgid':None,
                'sons':[]
            }
            
            ff['sons'] = n1(i)
            
            root.append(ff)
            
        else:
            continue
        pass

    return root

def jnn(n):
    """  排除不需要的类别

    Args:
        n (_type_): _description_

    Returns:
        _type_: _description_
    """
    if "Tout" in n:
        return True
    if "Tous" in n:
        return True
    else:
        return False



def n1(li):
    """找出二级目录

    Args:
        li (_type_): _description_
    """
    
    lis1 = li.xpath('./div/div/ul/li')[1:]
    n1s = []
    for i in lis1:
        try :
            name = i.xpath('./a/span/text()')[0].replace('\n','').replace(' ','')
        except:
            print('一级名称出错')
            name = i.xpath('./a/text()')
            if name == []:
                # name = "一级名称出错"
                continue
            else:
                name = name[0].replace('\n','').replace(' ','')
        dl = cd = None
        # jn = jnn(name)
        # if jn:
        #     continue
        ff = {
                'name':name,
                'data-url':dl,
                'cgid':cd,
                'sons':None
            }
        if dl == None:
            ff['sons'] = n2(i)
        n1s.append(ff)
    return n1s

def n2(li):
    """ 三级目录
    """
    lis1 = li.xpath('./div/ul/li')
    n1s = []
    for i in lis1:
        name = i.xpath('./a/text()')
        name = name[0].replace('\n','').replace(' ','')
        jn = jnn(name)
        if jn:
            continue
        # dl = 'https://www.gucci.com'+i.xpath('./a/@href')[0]
        du = i.xpath('./a/@href')[0]
        cd = None
        ff = {
                'name':name,
                'data-url':du,
                'cgid':cd,
                'sons':None
            }
        n1s.append(ff)
    return n1s

def ded(du):
    dus = du.split('/N-')
    return dus[-1]
    
def out():
    return get_html_404()



if __name__ == '__main__':
    get_html_404()

